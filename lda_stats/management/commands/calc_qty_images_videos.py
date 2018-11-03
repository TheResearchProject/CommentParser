# -*- coding: utf-8 -*-
import pdb
import re

from django.core.management.base import BaseCommand, CommandError
from django.db import connections

from comment_parser.queryset_iterator import queryset_iterator

from rss_parser.models import Text
from rss_parser.mycommand import MyCommand

class Command(MyCommand):
    help = 'Calculate the quantity of Images and Videos on newsitems'
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        images_re = re.compile("!\[(.+)\]\((.+)\)\n\n.+Photograph: .+\n\n")
        video_re = re.compile(u' – video[ \w\*]*')
        
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            cursor = connections[database].cursor()
            
            print "Grabbing newsitems and calculating..."
            queryset = Text.objects.using(database).filter(newsitem__isnull=False)
            
            self.pbar_setup(maxval=queryset.count())
            for text in queryset_iterator(queryset, chunksize=1000):
                new_text = ""
                
                subn = images_re.subn("", text.text)
                qty_images = subn[1]
                
                qty_videos = 0
                
                for line in subn[0].split("\n"):
                    if line.lower().strip() == "read more":
                        continue
                    elif line.lower().strip() == "facebook twitter pinterest":
                        continue
                    elif video_re.search(line):
                        qty_videos += 1
                    else:
                        new_text += line + "\n"
                        
                text.text = new_text
                text.save()
                        
                if qty_images > 0 or qty_videos > 0:
                    query = """
                    UPDATE newsitem
                       SET qty_images = %s,
                           qty_videos = %s
                     WHERE text_id = %s
                    """            
                    cursor.execute(query, [qty_images, qty_videos, text.id])
                
                self.pbar_increment()
            self.pbar_destroy()                  
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
           
