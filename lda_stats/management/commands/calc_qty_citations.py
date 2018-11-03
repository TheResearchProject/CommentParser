# -*- coding: utf-8 -*-
import pdb
import re

from django.db import connections

from comment_parser.queryset_iterator import queryset_iterator

from rss_parser.models import Text
from rss_parser.mycommand import MyCommand

class Command(MyCommand):
    help = 'Calculate the quantity of Images and Videos on newsitems'
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        citations_re = re.compile("\".*\"")
        
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            cursor = connections[database].cursor()
            
            print "Grabbing newsitems and calculating..."
            queryset = Text.objects.using(database).filter(newsitem__isnull=False)
            
            self.pbar_setup(maxval=queryset.count())
            for text in queryset_iterator(queryset, chunksize=1000):
                
                qty_citations = len(citations_re.findall(text.text))
                
                if qty_citations > 0:
                    query = """
                    UPDATE newsitem
                       SET qty_citations = %s
                     WHERE text_id = %s
                    """            
                    cursor.execute(query, [qty_citations, text.id])
                
                self.pbar_increment()
            self.pbar_destroy()                  
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
           
