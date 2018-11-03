# -*- coding: utf-8 -*-
from bisect import bisect_left

from nltk.tokenize.regexp import WordPunctTokenizer

from django.db import connections, transaction

from comment_parser.utils import dictfetch
from rss_parser.mycommand import MyCommand

class Command(MyCommand):
    help = 'Fill cat1_algorithm_date_comments table'
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            cursor = connections[database].cursor()
            update_cursor = connections[database].cursor()
            
            commands = []
            commands.append("TRUNCATE cat1_algorithm_date_comments")
            commands.append("""
            INSERT INTO cat1_algorithm_date_comments 
             (cat1_id, algorithm_id, date)
             SELECT cat1.id, algorithm.id, date
               FROM cat1, algorithm, dates
            """)
            
            for command in commands:
                self.stdout.write("Executing command: {}".format(command))
                cursor.execute(command)
            
            query = """
                SELECT cat1.id cat1_id, 
                       algorithm_id, 
                       DATE(newsitem.Date) ni_date, 
                       sentiment, 
                       count(*) amount
                  FROM cat1, newsitem, pos_neg_comments
                 WHERE cat1.id = newsitem.cat1
                   AND newsitem.id = pos_neg_comments.newsitem_id
                 GROUP BY cat1.id, algorithm_id, ni_date, sentiment
            """
            
            update_query = """
                UPDATE cat1_algorithm_date_comments
                   SET {} = %s
                 WHERE cat1_id = %s
                   AND algorithm_id = %s
                   AND date = %s
            """
            
            self.stdout.write("Grabbing data")
            cursor.execute(query)
            
            self.stdout.write("Updating cat1_algorithm_date_comments table")
            with transaction.atomic():
                self.pbar_setup(maxval=cursor.rowcount)
                for row in dictfetch(cursor):
                    if row['sentiment'] == -1:
                        column = "negative_comments"
                    elif row['sentiment'] == 0:
                        column = "neutral_comments"
                    elif row['sentiment'] == 1:
                        column = "positive_comments"
                    formatted_query = update_query.format(column)
                    update_cursor.execute(formatted_query, [
                        row['amount'],
                        row['cat1_id'],
                        row['algorithm_id'],
                        row['ni_date']
                    ])
                    self.pbar_increment()
                self.pbar_destroy()          
               
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
           
