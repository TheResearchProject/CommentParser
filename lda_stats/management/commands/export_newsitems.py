# -*- coding: utf-8 -*-
import codecs
import pdb
import os
import re

from django.core.management.base import BaseCommand, CommandError
from django.db import connections

from comment_parser.queryset_iterator import queryset_iterator

from rss_parser.models import Newsitem, Text
from rss_parser.mycommand import MyCommand, PathType

class Command(MyCommand):
    help = 'Dump the text of every newsitem into a text file with filename <dbname>_<newsitem_id>.txt into a specified directory.'
    
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('TARGET_DIR', type=PathType(exists=True, type='dir'), 
                                          help="Target directory of the dump")
                
    
    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)
        
        images_re = re.compile("!\[(.+)\]\((.+)\)")
        socials_re = re.compile("Facebook Twitter Pinterest")
        
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            cursor = connections[database].cursor()
            
            print "Grabbing newsitems and their texts, then dumping them to target folder ..."
            queryset = Newsitem.objects\
                               .using(database)\
                               .exclude(cat1__isnull=True)\
                               .only('date','cat1','title','text')\
                               
            
            self.pbar_setup(maxval=queryset.count())
            for newsitem in queryset_iterator(queryset, chunksize=1000):
                if not newsitem.text or not newsitem.text.text:
                    continue
                filename = "{}_{}_news_{}.txt".format(
                    newsitem.cat1,
                    newsitem.date.date().isoformat(),
                    newsitem.id)
                target_filename = os.path.join(options['TARGET_DIR'], filename)
                fileobj = codecs.open(target_filename, 'w', 'utf-8')
                fileobj.write(newsitem.title + ". \n" + newsitem.text.text)
                self.pbar_increment()
            self.pbar_destroy()                  
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
           
