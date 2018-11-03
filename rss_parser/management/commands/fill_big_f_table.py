# -*- coding: utf-8 -*-
from bisect import bisect_left

from nltk.tokenize.regexp import WordPunctTokenizer

from django.db import connections, transaction

from comment_parser.utils import dictfetch
from rss_parser.mycommand import MyCommand

class Command(MyCommand):
    help = 'Split author\'s names that are stored in DB comma-separated'
    def update_column(self, column, query):
        self.stdout.write("Updating {}".format(column))
        cursor = connections[self.database].cursor()
        update_cursor = connections[self.database].cursor()
        update_query = """
            UPDATE big_f_table 
               SET {} = %s
             WHERE cat1_id = %s
               AND date = %s
        """.format(column)
        
        cursor.execute(query)
        self.pbar_setup(maxval=cursor.rowcount)
        update_data = []
        for row in dictfetch(cursor):
            update_data.append([
                    row['result'],
                    row['cat1_id'],
                    row['item_date']
            ])
            if len(update_data) >= 5000:
                update_cursor.executemany(update_query, update_data)
                update_data = []
            self.pbar_increment()
        update_cursor.executemany(update_query, update_data)
        self.pbar_destroy()                
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            self.database = database
            
            self.update_column('number_of_news_items', 
                """
                SELECT cat1.id cat1_id, DATE(newsitem.date) item_date, count(*) result
                  FROM cat1, newsitem
                 WHERE cat1.id = newsitem.cat1
                 GROUP BY cat1.id, item_date
                """)
            
            self.update_column('number_of_comments', 
                """
                SELECT cat1.id cat1_id, DATE(comment.date) item_date, count(*) result
                  FROM cat1, newsitem, comment
                 WHERE cat1.id = newsitem.cat1
                   AND newsitem.Id = comment.NewsItemID
                 GROUP BY cat1.id, item_date
                """)
            
            self.update_column('number_of_likes', 
                """
                SELECT cat1.id cat1_id, DATE(newsitem.date) item_date, SUM(newsitem.Facebook) result
                  FROM cat1, newsitem
                 WHERE cat1.id = newsitem.cat1
                   AND newsitem.Facebook > 0
                 GROUP BY cat1.id, item_date       
                """)
            
            foo = [
                {'col': 'number_of_TG_DT_TFIDF_POS_comments','algo': 'TG_DT_TFIDF','result': " = 'POS'"},
                {'col': 'number_of_TG_DT_TFIDF_NEG_comments','algo': 'TG_DT_TFIDF','result': " = 'NEG'"},
                {'col': 'number_of_TG_DT_TFIDF_NEU_comments','algo': 'TG_DT_TFIDF','result': " = 'NEU'"},
                {'col': 'number_of_TG_KNN3_TFIDF_POS_comments','algo': 'TG_KNN3_TFIDF','result': " = 'POS'"},
                {'col': 'number_of_TG_KNN3_TFIDF_NEG_comments','algo': 'TG_KNN3_TFIDF','result': " = 'NEG'"},
                {'col': 'number_of_TG_KNN3_TFIDF_NEU_comments','algo': 'TG_KNN3_TFIDF','result': " = 'NEU'"},
                {'col': 'number_of_TG_NB_TFIDF_POS_comments','algo': 'TG_NB_TFIDF','result': " = 'POS'"},
                {'col': 'number_of_TG_NB_TFIDF_NEG_comments','algo': 'TG_NB_TFIDF','result': " = 'NEG'"},
                {'col': 'number_of_TG_NB_TFIDF_NEU_comments','algo': 'TG_NB_TFIDF','result': " = 'NEU'"},
                {'col': 'number_of_TG_afinn_POS_comments','algo': 'afinn','result': " > 0"},
                {'col': 'number_of_TG_afinn_NEG_comments','algo': 'afinn','result': " < 0"},     
                {'col': 'number_of_TG_afinn_NEU_comments','algo': 'afinn','result': " = 0"},
            ]
                    
            for bar in foo:
                self.update_column(bar['col'], 
                    """
                    SELECT cat1.id cat1_id, DATE(comment.date) item_date, count(*) result
                      FROM cat1, newsitem, comment, text, result, algorithm
                     WHERE cat1.id = newsitem.cat1
                       AND newsitem.Id = comment.NewsItemID
                       AND comment.text_id = text.id
                       AND text.id = result.text_id
                       AND result.algorithm_id = algorithm.id
                       AND algorithm.name = '{}'
                       AND result.value {}
                     GROUP BY cat1.id, item_date
                    """.format(bar['algo'], bar['result']))      
            foo = [
                {'col': 'avg_valence_comments','algo': 'anew_valence'},   
                {'col': 'avg_arousal_comments','algo': 'anew_arousal'},   
                {'col': 'avg_dominance_comments','algo': 'anew_dominance'}   
            ]
            
            for bar in foo:
                self.update_column(bar['col'], 
                    """
                    SELECT cat1.id cat1_id, DATE(comment.date) item_date, avg(result.value) result
                      FROM cat1, newsitem, comment, text, result, algorithm
                     WHERE cat1.id = newsitem.cat1
                       AND newsitem.Id = comment.NewsItemID
                       AND comment.text_id = text.id
                       AND text.id = result.text_id
                       AND result.algorithm_id = algorithm.id
                       AND algorithm.name = '{}'
                     GROUP BY cat1.id, item_date
                    """.format(bar['algo']))      
                
            foo = [
                {'col': 'avg_valence_news','algo': 'anew_valence'},   
                {'col': 'avg_arousal_news','algo': 'anew_arousal'},   
                {'col': 'avg_dominance_news','algo': 'anew_dominance'}   
            ]    
                
            for bar in foo:
                self.update_column(bar['col'], 
                    """
                    SELECT cat1.id cat1_id, DATE(newsitem.date) item_date, avg(result.value) result
                      FROM cat1, newsitem, text, result, algorithm
                     WHERE cat1.id = newsitem.cat1
                       AND newsitem.text_id = text.id
                       AND text.id = result.text_id
                       AND result.algorithm_id = algorithm.id
                       AND algorithm.name = '{}'
                     GROUP BY cat1.id, item_date
                    """.format(bar['algo']))       
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
           
