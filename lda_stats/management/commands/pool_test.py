# -*- coding: utf-8 -*-
import codecs
import csv
from decimal import *
import HTMLParser
import itertools
import math
from multiprocessing import Pool
import random
import pdb        
import re
import time

from rss_parser.mycommand import MyCommand

from comment_parser.queryset_iterator import queryset_iterator
from rss_parser.models import Algorithm, Result, Text

def work(i):
    time.sleep(i)

class Command(MyCommand):
    help = 'Test worker processing'
    
    def callback(self, dummy):
        print "callback!"
        #self.pbar_increment()
    
    def handle(self, *args, **options):    
        super(Command, self).handle(*args, **options)
        
        list_of_terms = [random.randint(1,3) for i in range(40)]
        
        pool = Pool()
        
        self.pbar_setup(maxval=len(list_of_terms))
        for _ in pool.imap_unordered(work, list_of_terms):
            self.pbar_increment()
    
        self.pbar_destroy()  
            
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))                