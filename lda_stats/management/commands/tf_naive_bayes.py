import copy
import cPickle
from multiprocessing import Pool, Process
import os
import pdb
import sys

from django.conf import settings
from django.db import connections

import nltk
from nltk.stem.wordnet import WordNetLemmatizer

from sklearn.naive_bayes import GaussianNB

from rss_parser.mycommand import MyCommand

from rss_parser.models import Algorithm, Result, Text

from comment_parser.queryset_iterator import queryset_iterator

import lda_stats.utils.idf as utils

print "Loading classifier"
classifier_path = os.path.join(
    settings.BASE_DIR, 
    "lda_stats/classifiers/tf_naive_bayes.classifier.cpickle")
nb = cPickle.load(open(classifier_path, 'rb'))

def estimate(text):
    return (text,
            nb.predict([utils.TFIDF_to_list(utils.TFIDF(utils.tokenize(text.text)))])
           )
    
def bulk_create(database, results):
    Result.objects.using(database).bulk_create(results)

class Command(MyCommand):
    help = ''
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        filters = {}
        if options['only_newsitems']:
            filters['newsitem__isnull'] = False
        elif options['only_comments']:
            filters['comment__isnull'] = False
            
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            
            algorithm_tf_naive_bayes, created = Algorithm.objects.using(database)\
                                                .get_or_create(name="tf_naive_bayes")

            print "Removing previous results"      
            query = """
            DELETE FROM result WHERE algorithm_id IN (
                SELECT id
                  FROM algorithm 
                 WHERE name = 'tf_naive_bayes'
            )"""            
            cursor = connections[database].cursor()
            cursor.execute(query)

            print "Querying database"
            queryset = Text.objects.using(database).filter(**filters)
            
            results = []
    
            self.pbar_setup(maxval=queryset.count())
            queryset_iter = queryset_iterator(queryset, chunksize=2000)
            
            print "Calculating..."
            
            bulk_create_process = None
            pool = Pool()
            
            for text, result in pool.imap_unordered(estimate, queryset_iter):
                results.append(Result(algorithm=algorithm_tf_naive_bayes,
                                      text=text,
                                      value=str(result[0])))
                self.pbar_increment()
                
                if len(results) >= 10000:
                    if bulk_create_process and bulk_create_process.is_alive():
                        bulk_create_process.join()
                    bulk_create_process = Process(
                        target=bulk_create,
                        kwargs={'database': database,
                                'results': copy.copy(results)}
                    )
                    bulk_create_process.start()
                    results = []
    
            self.pbar_destroy()       
            
            print "Saving results"
            Result.objects.using(database).bulk_create(results)
            
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
