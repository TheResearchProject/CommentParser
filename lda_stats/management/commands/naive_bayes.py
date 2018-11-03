import cPickle
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

class Command(MyCommand):
    help = ''
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        print "Loading classifier"
        classifier_path = os.path.join(
            settings.BASE_DIR, 
            "lda_stats/classifiers/naive_bayes.classifier.cpickle")
        nb = cPickle.load(open(classifier_path, 'rb'))
        
        filters = {}
        if options['only_newsitems']:
            filters['newsitem__isnull'] = False
        elif options['only_comments']:
            filters['comment__isnull'] = False
            
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            
            algorithm_naive_bayes, created = Algorithm.objects.using(database)\
                                                .get_or_create(name="naive_bayes")

            print "Removing previous results"      
            query = """
            DELETE FROM result WHERE algorithm_id IN (
                SELECT id
                  FROM algorithm 
                 WHERE name = 'naive_bayes'
            )"""            
            cursor = connections[database].cursor()
            cursor.execute(query)

            print "Querying database"
            queryset = Text.objects.using(database).filter(**filters)
            
            results = []
    
            print "Calculating..."
            self.pbar_setup(maxval=queryset.count())
            for text in queryset_iterator(queryset, chunksize=2000):
                estimate=nb.predict([utils.TFIDF_to_list(utils.TFIDF(utils.tokenize(text.text)))])
                results.append(Result(algorithm=algorithm_naive_bayes,
                                      text=text,
                                      value=str(estimate[0])))
                self.pbar_increment()
                
                if len(results) > 100000:
                    print "\nSaving partial results..."
                    Result.objects.using(database).bulk_create(results)
                    results = []                  
                
            self.pbar_destroy()       
            
            print "Saving results"
            Result.objects.using(database).bulk_create(results)
            
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
