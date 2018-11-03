from collections import Counter
import cPickle
from multiprocessing import Pool
import pdb
import os.path

from nltk.tokenize import RegexpTokenizer
import networkx
import MySQLdb

from bulk_update.helper import bulk_update

from django.conf import settings
from django.db import connections

from comment_parser.utils import TextCleaner, dictfetch
from comment_parser.queryset_iterator import queryset_iterator    
from rss_parser.models import Algorithm, Author, Comment, Newsitem, Result, Text
from rss_parser.mycommand import MyCommand

tokenizer = RegexpTokenizer(r'\w+')
text_cleaner = TextCleaner() 
        
def tokenize(item):
    clean_text = text_cleaner.clean(item.text.text)
    return item, tokenizer.tokenize(clean_text)                         

class Command(MyCommand):
    help = 'Get summarized data from authors'
    items_used = "*"

    def handle(self, *args, **options):        
        self.stdout.write('Command started')      
        super(Command, self).handle(self, *args, **options)
        
        #self.edges = []
        #
        #self.stdout.write("Connecting manually to target database")
        #targetdb_conn = MySQLdb.connect(
        #    host  = settings.GENERAL_DATA_DB_DETAILS['HOST'],
        #    user  = settings.GENERAL_DATA_DB_DETAILS['USER'],
        #    passwd= settings.GENERAL_DATA_DB_DETAILS['PASSWORD'],
        #    db    = settings.GENERAL_DATA_DB_DETAILS['NAME'],
        #    port  = settings.GENERAL_DATA_DB_DETAILS['PORT'],
        #    charset = 'utf8',
        #    use_unicode = True                               
        #)                   
        #targetdb_cursor = targetdb_conn.cursor()
        #
        #select_query = """
        #    SELECT * FROM author_analysis WHERE newssite = %s        
        #"""                          
        
        for database in self.selected_dbs:                      
            self.stdout.write("Processing database "+database)
            
            self.authors = {}
            queryset = Author.objects.using(database).all()
            if queryset.count() > 0:
                self.stdout.write("Reading authors")   
                self.pbar_setup(maxval=queryset.count())
                queryset_iter = queryset_iterator(queryset, chunksize=1000)
                for author in queryset_iter:
                    self.authors[author.name] = author
                    self.pbar_increment()
                self.pbar_destroy()                  
                
            for model in [Comment, Newsitem]:
                
                if model == Comment: 
                    model_name = "Comment"
                    filters = {'authorshortname__isnull': False, 'author__isnull':True}
                else:
                    model_name = "Newsitem"
                    filters = {'idauthor__isnull': False, 'author__isnull':True}
                self.stdout.write("Processing model " + model_name)
                
                queryset = model.objects.using(database)\
                                        .filter(**filters)
                                        
                self.stdout.write('Linking Authors with ' + model_name)
                
                if queryset.count() == 0:
                    self.stdout.write('No authors to link')
                    continue
                self.pbar_setup(maxval=queryset.count())
                queryset_iter = queryset_iterator(queryset, chunksize=1000)
                
                for item in queryset_iter:
                    if model == Comment:
                        if item.authorshortname in self.authors:
                            item.author = self.authors[item.authorshortname]
                        else:
                            le_author = Author.objects.using(database).create(
                                name = item.authorshortname,
                                long_name = item.authorid
                            )
                            item.author = le_author
                            self.authors[item.authorshortname] = le_author
                    else:
                        if item.idauthor in self.authors:
                            item.author = self.authors[item.idauthor]
                        else:
                            le_author = Author.objects.using(database).create(
                                name = item.idauthor
                            )
                            item.author = le_author
                            self.authors[item.idauthor] = le_author   
                    item.save()
                    self.pbar_increment()
                self.pbar_destroy()                                
                            
                bulk_update(queryset, 
                            batch_size=1000,
                            using=database,
                            update_fields=['author'])   
            
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
