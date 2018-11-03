import nltk
from nltk.stem.wordnet import WordNetLemmatizer

import pdb
import random

from rss_parser.mycommand import MyCommand

from rss_parser.models import Newsitem, Algorithm, Result

from comment_parser.queryset_iterator import queryset_iterator

import lda_stats.utils.idf as utils

class Command(MyCommand):
    help = ''
    
    def handle(self, *args, **options):
        
        queryset = Newsitem.objects
        self.pbar_setup(maxval=queryset.count())
        newsitems = queryset_iterator(queryset.all(),chunksize=100)
        
        for newsitem in newsitems:
            newsitem.cat1 = random.randint(1, 5)
            newsitem.save()
            self.pbar_increment()
            
        self.pbar_destroy()
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
