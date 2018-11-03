# -*- coding: utf-8 -*-
import codecs
import pdb
import os
import re

from django.core.management.base import BaseCommand, CommandError
from django.db import connections

from comment_parser.queryset_iterator import queryset_iterator

from rss_parser.models import Comment, Newsitem, Text
from rss_parser.mycommand import MyCommand, PathType

class Command(MyCommand):
    help = 'Dump the text of every comment into a text file with filename <dbname>_<comment_id>.txt into a specified directory.'
    
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('TARGET_DIR_ALL', type=PathType(exists=True, type='dir'), 
                                              help="Target directory of the dump for ALL comments")        
        parser.add_argument('TARGET_DIR_NEWS', type=PathType(exists=True, type='dir'), 
                                              help="Target directory of the dump for comments that are connected directly to a newsitem (no parent comment)")
                
    
    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)
        
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            cursor = connections[database].cursor()
            
            print "Grabbing newsitems data"
            queryset = Newsitem.objects\
                               .using(database)\
                               .exclude(cat1__isnull=True)\
                               .only('cat1')
            newsitems_cat1 = {}
            
            self.pbar_setup(maxval=queryset.count())
            for newsitem in queryset_iterator(queryset, chunksize=1000):
                if newsitem.cat1 == None:
                    pdb.set_trace()
                    pass
                newsitems_cat1[newsitem.id] = newsitem.cat1
                self.pbar_increment()
            self.pbar_destroy()
            
            print "Grabbing comments and their texts, then dumping them to target folder ..."
            queryset = Comment.objects\
                              .using(database)\
                              .filter(newsitem_id__in=newsitems_cat1.keys())\
                              .only('date','newsitem_id','parent_id','text')
            
            self.pbar_setup(maxval=queryset.count())
            for comment in queryset_iterator(queryset, chunksize=1000):
                if not comment.text or not comment.text.text:
                    continue
                cat1 = newsitems_cat1[comment.newsitem_id]
                if cat1 == None:
                    pdb.set_trace()
                    pass
                filename = "{}_{}_{}.txt".format(
                    cat1,
                    comment.date.date().isoformat(),
                    comment.id)
                target_filename = os.path.join(options['TARGET_DIR_ALL'], filename)
                fileobj = codecs.open(target_filename, 'w', 'utf-8')
                fileobj.write(comment.text.text)         
                fileobj.close()
                if comment.parent_id == None:
                    target_filename = os.path.join(options['TARGET_DIR_NEWS'], filename)
                    fileobj = codecs.open(target_filename, 'w', 'utf-8')
                    fileobj.write(comment.text.text)         
                    fileobj.close()                    
                self.pbar_increment()
            self.pbar_destroy()                  
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
           
