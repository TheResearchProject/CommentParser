# -*- coding: utf-8 -*-
import pdb

from django.db import connections, transaction

from comment_parser.utils import dictfetch
from rss_parser.mycommand import MyCommand

class Command(MyCommand):
    help = 'Split author\'s names that are stored in DB comma-separated'
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            cursor = connections[database].cursor()
            
            get_faulty_authors_query = """
                SELECT id, name FROM author WHERE name LIKE '%,%'
            """             
            
            insert_author_query = """
                INSERT IGNORE INTO author (name) VALUES (%s)
            """
            
            insert_newsite_author_query = """
                INSERT IGNORE INTO author_newsitem (author_id, newsitem_id) 
                SELECT DISTINCT author.id, an_old_author.newsitem_id 
                  FROM author_newsitem an_new_author, 
                       author_newsitem an_old_author, 
                       author
                 WHERE an_new_author.author_id = author.id
                   AND author.name = %s
                   AND an_old_author.author_id = %s
            """
            
            cursor = connections[database].cursor()
            
            cursor.execute(get_faulty_authors_query)
            
            with transaction.atomic():
                self.pbar_setup(maxval=cursor.rowcount)
                insert_cursor = connections[database].cursor()
                for row in dictfetch(cursor):
                
                    authors = row['name'].split(',')
                    
                    for author in authors:
                        insert_cursor.execute(insert_author_query, [author])
                        insert_cursor.execute(insert_newsite_author_query, 
                                              [author, row['id']])
                
                    self.pbar_increment()
                self.pbar_destroy()                  
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
           
