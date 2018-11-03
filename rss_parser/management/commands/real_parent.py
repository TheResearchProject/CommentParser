# -*- coding: utf-8 -*-
from bisect import bisect_left

from nltk.tokenize.regexp import WordPunctTokenizer

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
            
            get_authors_query = """
                SELECT name, long_name
                  FROM author
            """             
            
            get_comments_query = """
                SELECT id, content FROM comment
            """
            
            cursor = connections[database].cursor()
            tokenizer = WordPunctTokenizer()
            
            self.stdout.write("Grabbing authors...")
            authors = []
            cursor.execute(get_authors_query)
            self.pbar_setup(maxval=cursor.rowcount)
            for row in dictfetch(cursor):
                authors.append(row['name'])
                if row['long_name'] != "":
                    authors.append(row['long_name'])
                self.pbar_increment()
            self.pbar_destroy()                      
            
            self.stdout.write("Sorting authors...")
            authors.sort()
            
            self.stdout.write("Determining real parents...")
            real_parents = []
            cursor1 = connections[database].cursor()
            cursor1.execute(get_comments_query)
            self.pbar_setup(maxval=cursor1.rowcount)
            for row in dictfetch(cursor1):
                tokens = tokenizer.tokenize(row['content'])
                if len(tokens) > 0:
                    if tokens[0] == '@':
                        real_parents.append(int(row['id']))
                    else:
                        i = bisect_left(authors, tokens[0])
                        if i != len(authors) and authors[i] == tokens[0]:
                            real_parents.append(int(row['id']))
                
                self.pbar_increment()
            self.pbar_destroy()       
            
            self.stdout.write("Non-Real-parents found: {}".format(len(real_parents)))
            
            cursor2 = connections[database].cursor()
            update_query = """
                UPDATE comment 
                   SET real_parent = (CASE WHEN id in ({}) THEN 0 ELSE 1 END)            
            """.format(('%s,'*len(real_parents)).rstrip(','))
            cursor2.execute(update_query, real_parents)
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
           
