import os
import tempfile
import time
import shutil

import pdb

import gensim
from gensim.corpora import BleiCorpus, Dictionary

from rss_parser.mycommand import MyCommand
from rss_parser.models import Word, Comment, Algorithm, Result

from comment_parser.queryset_iterator import queryset_iterator

class Corpus():
    def __init__(self, collection, dictionary):
        self.collection = collection
        self.dictionary = dictionary
        
    def __iter__(self):
        for item in self.collection:
            if hasattr(item, 'word_set'):
                lst = [word.word for word in item.word_set.all()]
                yield self.dictionary.doc2bow(lst)

class Command(MyCommand):
    help = 'Calculate the hot topics'
    
    def handle(self, *args, **options): 
        super(Command, self).handle(self, *args, **options)
        
        #Create temporary directory to write the corpus LDA-C files
        temp_dir_path = tempfile.mkdtemp()
        corpus_path = temp_dir_path + "/corpus.lda-c"
        
        lda_num_topics = 50
        
        for database in self.selected_dbs:    
            
            print "Processing database " + database

            #Building dictionary
            print "Building dictionary"
            dictionary = Dictionary()
            
            queryset = Comment.objects.using(database).exclude(text__isnull=True)
            self.pbar_setup(maxval=queryset.count())
            
            for comment in queryset_iterator(queryset ,chunksize=50):
                dictionary.add_documents([[word.word for word in comment.text.word_set.all()]])
                self.pbar_increment()          
            self.pbar_destroy()
                
            dictionary.filter_extremes(keep_n=10000)
            dictionary.compactify()
            
            #Serialize corpus
            print "Serializing corpus"
            corpus = Corpus(queryset_iterator(Comment.objects.using(database).all(), chunksize=50), dictionary)
            BleiCorpus.serialize(corpus_path, corpus, id2word=dictionary)
            
            #Train
            print "Training..."
            bleicorpus = BleiCorpus(corpus_path)
            lda = gensim.models.LdaModel(bleicorpus, 
                                         num_topics=lda_num_topics, 
                                         id2word=dictionary)
            
            #Saving
            print "Saving results to DB"
            lda_db_obj, created = Algorithm.objects.using(database).get_or_create(name='LDA')
            #Removing previous results
            lda_db_obj.result_set.all().delete()
            #Looping through results and saving to DB
            i = 0
            for topic in lda.show_topics(num_topics=lda_num_topics):
                Result.objects.using(database).create(sequence=i, 
                                                      value=str(topic), 
                                                      algorithm=lda_db_obj)
                i += 1
                    
            #Remove temporary directory
            #Check first if it's not the current working directory, as removing it
            #  would be a disaster! ;)
            if os.getcwd() != temp_dir_path:
                #Just remove it if it's a temp dir
                shutil.rmtree(temp_dir_path)
            else:
                #If it's the current working directory, just remove the uneeded files    
                map(os.remove, glob.glob('corpus.lda-c*'))
                    
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
