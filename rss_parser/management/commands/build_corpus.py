from collections import deque 
import cPickle
import itertools
import pdb
import random

from gensim.models.word2vec import Word2Vec

from nltk.tokenize import RegexpTokenizer

from progressbar import ProgressBar, \
    SimpleProgress, FormatLabel, ETA, Percentage, Bar, Timer, AdaptiveETA

from django.core.management.base import CommandError
from django.db import transaction, connections

from comment_parser.queryset_iterator import queryset_iterator    

from comment_parser.multi_db_iterator import MultiDbIterator
from rss_parser.models import Text
from rss_parser.mycommand import MyCommand

class Progress():
    def __init__(self, maxval, console=False):
        self.done = 0
        if console:
            pbar_widgets = [FormatLabel('Processed: %(value)d/%(max)d items (in: %(elapsed)s)'), 
               ' -=- ', Percentage(),
               ' -=- ', ETA()]  
            self.pbar = ProgressBar(widgets=pbar_widgets, 
                                    maxval=maxval, 
                                    endline_character="\n")           
        else:
            pbar_widgets = [SimpleProgress(),
               ' ', Percentage(),
               ' ', Bar(),
               ' ', Timer(),
               ' ', AdaptiveETA()]   
            self.pbar = ProgressBar(widgets=pbar_widgets, 
                                maxval=maxval)
        if console:
            self.pbar.update_interval = 50000
        self.pbar.start()         
        
    def pbar_increment(self):
        self.done += 1
        self.pbar.update(self.done)  
        
    def pbar_destroy(self):
        self.pbar.finish()

class IterTexts:
    
    def __init__(self, databases, filters, chunksize = 1000):
        
        self.tokenizer = RegexpTokenizer(r'\w+')
        print "Opening cursor"
        self.cursor = connections['auxiliar'].cursor()
        self.chunksize = chunksize
        
        print "Getting count"
        query = "SELECT count(*) FROM text"
        self.cursor.execute(query)
        result = self.cursor.fetchone()      
        self.total_items = result[0]    
        
    def set_pbar(self, pbar):
        self.pbar = pbar
        
    def first(self):    
        self.text_ids = range(self.total_items)
        random.shuffle(self.text_ids)        
        self.fetch()
        
    def fetch(self):
        if len(self.text_ids) > 0:
            ids = ",".join([str(i) for i in self.text_ids[:self.chunksize]])
            query = "SELECT text FROM text WHERE id IN ({})".format(ids)
            self.cursor.execute(query)
            self.queryset = deque(self.cursor.fetchall())      
            del self.text_ids[:self.chunksize]   
        else:
            raise StopIteration()
        
    def __iter__(self):
        return self
        
    def next(self):
        try:
            tokens = self.tokenizer.tokenize(self.queryset.pop()[0])
            self.pbar.increment()
            return tokens
        except IndexError:
            self.fetch()
            return self.next()

class Command(MyCommand):
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        self.stdout.write(self.style.SUCCESS('Starting up'))  
        
        epochs = 10 
        chunksize = 2000
        
        filters = {}
        if options['only_newsitems']:
            filters['newsitem__isnull'] = False
        elif options['only_comments']:
            filters['comment__isnull'] = False   
             
        iter_texts = IterTexts(databases=self.selected_dbs, 
                               filters=filters,
                               chunksize=chunksize)
        
        self.stdout.write("Loading dictionary")
        self.pbar_setup(maxval=iter_texts.total_items)
        iter_texts.set_pbar(self.pbar)
        iter_texts.first()
        word2vec = Word2Vec(iter_texts)
        self.pbar_destroy()   
        self.stdout.write(self.style.SUCCESS("Dictionary loaded succesfully"))
        
        self.stdout.write("Traning...")
        
        for epoch in range(1, epochs+1):
            self.stdout.write("Running epoch #{}".format(epoch))    
            iter_texts.first()
            self.pbar_setup(maxval=iter_texts.total_items)
            iter_texts.set_pbar(self.pbar)            
            word2vec.train(iter_texts)
            self.pbar_destroy()   
        
        self.stdout.write(self.style.SUCCESS("Saving model"))
        word2vec.save('newsitems.word2vec')
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))            