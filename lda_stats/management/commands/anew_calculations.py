# -*- coding: utf-8 -*-
import codecs
import copy
import csv
from decimal import *
import HTMLParser
import itertools
import math
from multiprocessing import Pool, Process
import pdb        
import re

from django.db import connections

from rss_parser.mycommand import MyCommand

from comment_parser.multi_db_iterator import MultiDbIterator
from comment_parser.queryset_iterator import queryset_iterator
from rss_parser.models import Algorithm, Result, Text

wordlist = {}

print "Reading ANEW.csv data"

for row in csv.DictReader(open('ANEW.csv')):
    wordlist[row['Description']] = {
        'valence_mean': Decimal(row['Valence Mean']),
        'valence_sd': Decimal(row['Valence SD']),
        'arousal_mean': Decimal(row['Arousal Mean']),
        'arousal_sd': Decimal(row['Arousal SD']),
        'dominance_mean': Decimal(row['Dominance Mean']),
        'dominance_sd': Decimal(row['Dominance SD'])
    }    

def bulk_create(database, results):
    Result.objects.using(database).bulk_create(results)

def calculate(array):
    """
    Takes a list of 2-element tuples with the data (std.deviation, mean sum),
    and returns the score based on the weight of each tuple
    """
    #An illustration of what is about to happen:
    #>>> a = [2,7,4,6,1]
    #>>> a.sort()                                                         
    #>>> a
    #[1, 2, 4, 6, 7]
    #>>> a[::-1] <-- this is how you invert a list in python :)
    #[7, 6, 4, 2, 1]    
    #>>> for x,y in itertools.izip(a, a[::-1]): print "{},{}".format(x,y)                                                                       
    #1,7                                                                                                                                        
    #2,6                                                                                                                                        
    #4,4                                                                                                                                        
    #6,2                                                                                                                                        
    #7,1
    # Sum the standard deviations
    coeficient_sum = sum([i[0] for i in array])
    # Sort the input list by the firts element of each tuple
    array.sort(key=lambda tup: tup[0])
    # This variable will hold the sum of the resulting score
    result = 0         
    # Here's the tricky part: we use itertools like the example above
    #   to iterate over the sorted array and it's inverted copy.
    #   sa1 = sorted array 1st value (std.deviation)
    #   sa2 = sorted array 2nd value (mean sum)
    #   isa1 = inverted sorted array 1st value (std.deviation)
    #   isa2 = inverted sorted array 2nd value (mean sum)  
    for item,opposite_item in itertools.izip(array, array[::-1]):
        sa2 = item[1]
        isa1 = opposite_item[0]
        result += (isa1/coeficient_sum)*sa2
    return result
    
html_parser = HTMLParser.HTMLParser()    
    
def clean_text(text):
    text = html_parser.unescape(text)
    text = re.sub('@[\w_]+','',text)
    text = re.sub('(https?://[\w\.\/\?&=]+)\s?','',text)
    text = re.sub('[^\w\s#_\']',' ',text)
    text = re.sub('\s{2,9999}',' ',text)
    return text.lower()       

def work(text):
    results = None
    
    text_words = clean_text(text.text).split()
    
    #Filter words that are not in our wordlist
    words = []
    for word in text_words:
        if word in wordlist:
            words.append(word)

    #Calculate only if there are more than two matching words            
    if len(words) > 2:

        arousal_array = []
        valence_array = []
        dominance_array = []          
    
        for word in words:
            word_data = wordlist[word]
            arousal_array.append((word_data['arousal_sd'],word_data['arousal_mean']))
            valence_array.append((word_data['valence_sd'],word_data['valence_mean']))
            dominance_array.append((word_data['dominance_sd'],word_data['dominance_mean']))
    
        arousal =   str(calculate(arousal_array)  )
        valence =   str(calculate(valence_array)  )
        dominance = str(calculate(dominance_array))
        
        results = {
            'arousal'  : arousal,
            'valence'  : valence,
            'dominance': dominance
        }
        
    return text, results

class Command(MyCommand):
    help = 'Calculate the hot topics'
    
    def handle(self, *args, **options):    
        super(Command, self).handle(*args, **options)
        
        filters = {}
        if options['only_newsitems']:
            filters['newsitem__isnull'] = False
        elif options['only_comments']:
            filters['comment__isnull'] = False
            
        bulk_create_process = None
            
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            
            algorithm_anew_valence, _ = Algorithm.objects.using(database)\
                                    .get_or_create(name="anew_valence")
            algorithm_anew_arousal, _ = Algorithm.objects.using(database)\
                                                .get_or_create(name="anew_arousal")
            algorithm_anew_dominance, _ = Algorithm.objects.using(database)\
                                                .get_or_create(name="anew_dominance")  
            
            queryset = Text.objects.using(database).filter(**filters)
            
            print "Removing previous results"      
            query = """
            DELETE FROM result WHERE algorithm_id IN (
                SELECT id
                  FROM algorithm 
                 WHERE name IN ('anew_valence',  
                                'anew_arousal', 
                                'anew_dominance')
            )"""            
            cursor = connections[database].cursor()
            cursor.execute(query)
            results = []
            
            queryset_iter = queryset_iterator(queryset, chunksize=10000)
                         
            print "Calculating..."
            self.pbar_setup(maxval=queryset.count())
            
            pool = Pool()   
            
            for text, work_results in pool.imap_unordered(work, queryset_iter):
                                              
                if work_results != None:
                    results.append(Result(algorithm=algorithm_anew_arousal,
                                          text=text,
                                          value=work_results['arousal']))               
                    results.append(Result(algorithm=algorithm_anew_valence,
                                          text=text,
                                          value=work_results['valence']))
                    results.append(Result(algorithm=algorithm_anew_dominance,
                                          text=text,
                                          value=work_results['dominance'])) 
                    
                if len(results) > 10000:
                    if bulk_create_process and bulk_create_process.is_alive():
                        bulk_create_process.join()
                    bulk_create_process = Process(
                        target=bulk_create,
                        kwargs={'database': database,
                                'results': copy.copy(results)}
                    )
                    bulk_create_process.start()
                    results = []
                self.pbar_increment()
        
            self.pbar_destroy()  
            
            print "Saving last results..."
            Result.objects.using(database).bulk_create(results)  
            results = []  
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))                