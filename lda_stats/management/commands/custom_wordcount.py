# -*- coding: utf-8 -*-
import codecs
from multiprocessing import Pool, Process

from comment_parser.queryset_iterator import queryset_iterator
from word_processing.text_parser import TextProcessor                                                

from rss_parser.models import Newsitem, Comment
from rss_parser.mycommand import MyCommand     

text_processor = TextProcessor()
def count_words(item):
    wordcount = {}
    for word_type, word in text_processor.parse_text(item.text.text):
        if word_type == "word":
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
                
    return wordcount

class Command(MyCommand):
    help = 'Calculate the amount of positive and negative comments on newsitems'   
    
    def merge_wordcount(self, wordcount):
        for word, count in wordcount.items():
            if word in self.wordcount:
                self.wordcount[word] += count
            else:
                self.wordcount[word] = count
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        for database in self.selected_dbs:    
            
            print "Processing database " + database

            pool = Pool()
            
            #print "Wordcounting newsitems"
            #self.wordcount = {}    
            #
            #queryset = Newsitem.objects.using(database).select_related('text')\
            #                                           .filter(text__isnull=False)
            #queryset_iter = queryset_iterator(queryset, chunksize=25)                                                       
            #
            #self.pbar_setup(maxval=queryset.count())
            #for wordcount in pool.imap_unordered(count_words, queryset_iter):
            #    self.merge_wordcount(wordcount)   
            #    self.pbar_increment()
            #self.pbar_destroy()            
            #
            #output = codecs.open('wordcount_newsitems.csv', 'w', 'utf-8')
            #output.write("word,count\n")
            #
            #for word, count in self.wordcount.items():
            #    output.write("{},{}\n".format(word,count))            

            print "Wordcounting comments"
            self.wordcount = {}    

            queryset = Comment.objects.using(database).select_related('text')\
                                                       .filter(text__isnull=False)
            queryset_iter = queryset_iterator(queryset, chunksize=100)                                                       
            
            self.pbar_setup(maxval=queryset.count())
            for wordcount in pool.imap_unordered(count_words, queryset_iter):
                self.merge_wordcount(wordcount)   
                self.pbar_increment()
            self.pbar_destroy()                
            
            output = codecs.open('wordcount_comments.csv', 'w', 'utf-8')
            output.write("word,count\n")
            
            for word, count in self.wordcount.items():
                output.write(u"{},{}\n".format(word,count))

        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
           
