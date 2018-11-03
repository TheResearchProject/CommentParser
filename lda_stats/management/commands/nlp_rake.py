# -*- coding: utf-8 -*-
import copy
import HTMLParser
from multiprocessing import Pool, Process

from django.db import connections

from nltk.stem.porter import PorterStemmer

import comment_parser.rake as rake
from rss_parser.mycommand import MyCommand
from comment_parser.queryset_iterator import queryset_iterator
from rss_parser.models import Algorithm, Keyword, Text

def bulk_create(database, results):
    Keyword.objects.using(database).bulk_create(results)
    
raker = rake.Rake('stopwords.txt')    
stemmer = PorterStemmer()
html_parser = HTMLParser.HTMLParser()    
    
def clean_text(text):
    text = html_parser.unescape(text)
    text = re.sub('@[\w_]+','',text)
    text = re.sub('(https?://[\w\.\/\?&=]+)\s?','',text)
    text = re.sub('[^\w\s#_\.]',' ',text)
    text = re.sub('\s{2,9999}',' ',text)
    return text.lower()  

def work(text):
    
    current_word = ""
    stemmed_sentence = ""    
    
    for letter in text.text.lower():
        if letter.isalpha():
            current_word += letter
        else:
            if len(current_word) > 0:
                stemmed_sentence += stemmer.stem(current_word)
                current_word = ""
            stemmed_sentence += letter    
    
    return raker.run(stemmed_sentence)

class Command(MyCommand):
    help = 'Calculate the hot topics'
    
    def handle(self, *args, **options):    
        super(Command, self).handle(*args, **options)
        
        filters = {}
        if options['only_newsitems']:
            filters['newsitem__isnull'] = False
        elif options['only_comments']:
            filters['comment__isnull'] = False
            
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            
            algorithm_nlp_rake, _ = Algorithm.objects.using(database)\
                                                 .get_or_create(name="nlp_rake")
            
            queryset = Text.objects.using(database).filter(**filters)
            
            print "Removing previous results"      
            query = """
            DELETE FROM keyword WHERE algorithm_id = %s
            """            
            cursor = connections[database].cursor()
            cursor.execute(query, [algorithm_nlp_rake.id])
            
            queryset_iter = queryset_iterator(queryset, chunksize=1000)
            
            print "Calculating..."
            self.pbar_setup(maxval=queryset.count())
            
            results = []
            
            pool = Pool()  
            bulk_create_process = None
            
            for text in queryset_iter:
                keywords = work(text)      
                for keyword, score in keywords:
                    results.append(Keyword(
                        algorithm = algorithm_nlp_rake,  
                        text = text,  
                        keyword = keyword,  
                        score = score,  
                    ))
                              
                    if len(results) > 250:
                        Keyword.objects.using(database).bulk_create(results) 
                        results = []   
                        
                self.pbar_increment()
        
            self.pbar_destroy()  
            
            if len(results) > 0:
                print "Saving last results..."
                Keyword.objects.using(database).bulk_create(results)  
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))                