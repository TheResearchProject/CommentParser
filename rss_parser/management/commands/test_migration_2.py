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
from rss_parser.models import Algorithm, Author, AuthorSummary
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
        
        self.stdout.write("Connecting manually to target database")
        targetdb_conn = MySQLdb.connect(
            host  = settings.GENERAL_DATA_DB_DETAILS['HOST'],
            user  = settings.GENERAL_DATA_DB_DETAILS['USER'],
            passwd= settings.GENERAL_DATA_DB_DETAILS['PASSWORD'],
            db    = settings.GENERAL_DATA_DB_DETAILS['NAME'],
            port  = settings.GENERAL_DATA_DB_DETAILS['PORT'],
            charset = 'utf8',
            use_unicode = True                               
        )                   
        targetdb_cursor = targetdb_conn.cursor()
        
        select_query = """
            SELECT * FROM author_analysis WHERE newssite = %s        
        """                          
        
        for database in self.selected_dbs:                      
            self.stdout.write("Processing database "+database)
            
            self.stdout.write("Reading authors")   
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
            
            self.stdout.write("Moving data...")  
            targetdb_cursor.execute(select_query, [database])
            
            self.pbar_setup(maxval=targetdb_cursor.rowcount)
            
            results = []
            
            for row in dictfetch(targetdb_cursor):  
                if row['author'] in self.authors:
                    le_author = self.authors[row['author']]
                else:
                    le_author = Author.objects.using(database).create(
                        name = row['author']
                    )
                    self.authors[item.idauthor] = le_author                     
                results.append(AuthorSummary(
                    author = le_author,
                    avg_nr_words = row['avg_nr_words'],
                    avg_wordlen = row['avg_wordlen'],
                    avg_words_gt6 = row['avg_words_gt6'],
                    avg_personal = row['avg_personal'],
                    avg_collective = row['avg_collective'],
                    indegree = row['indegree'],
                    indegree_centrality = row['indegree_centrality'],
                    outdegree = row['outdegree'],
                    outdegree_centrality = row['outdegree_centrality'],
                    degree = row['degree'],
                    degree_centrality = row['degree_centrality'],
                    avg_shared = row['avg_shared'],
                    pagerank = row['pagerank'],
                    pagerank_weighted = row['pagerank_weighted'],
                    nr_posts = row['nr_posts'],
                    hub_score = row['hub_score'],
                    authority_score = row['authority_score'],
                    betweeness_centrality = row['betweeness_centrality'],
                    closeness_centrality = row['closeness_centrality'],
                    clustering_coef = row['clustering_coef'],
                    eccentricity = row['eccentricity'],
                    constraint = row['constraint'],
                    polarity_arousal = row['polarity_arousal'],
                    polarity_valence = row['polarity_valence'],                    
                ))
                if len(results) >= 1000:
                    AuthorSummary.objects.using(database).bulk_create(results)
                    results = []
                self.pbar_increment()
            self.pbar_destroy()  
            
            if len(results) > 0:
                AuthorSummary.objects.using(database).bulk_create(results)
            
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
