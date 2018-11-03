# -*- coding: utf-8 -*-
from collections import Counter
import pdb
import re

from django.db import connections, transaction

from comment_parser.queryset_iterator import queryset_iterator
from api.comparator import comparator

from comment_parser.utils import dictfetch
from rss_parser.models import Algorithm
from rss_parser.mycommand import MyCommand

POSITIVE_COMMENT = 1
NEGATIVE_COMMENT = -1
NEUTRAL_COMMENT = 0

class Command(MyCommand):
    help = 'Calculate the amount of positive and negative comments on newsitems'    
    
    def do_compare(self, formula, raw_value):
        value = raw_value
        if formula[0:2] != '="':
            value = float(value)
        return comparator(formula, value)      
    
    def check_result(self, algorithm, value):    
        if self.do_compare(algorithm.positive_formula, value):
            return POSITIVE_COMMENT
        elif self.do_compare(algorithm.neutral_formula, value):   
            return NEUTRAL_COMMENT  
        elif self.do_compare(algorithm.negative_formula, value):         
            return NEGATIVE_COMMENT
        else:
            raise Exception("No valid formula for value {} using algorithm {}".format(
                value, 
                algorithm.name))
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        citations_re = re.compile("\".*\"")
        
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            cursor = connections[database].cursor()
            
            algorithm_list = ['afinn', 
                              'TG_KNN3_TFIDF', 
                              'TG_DT_TFIDF', 
                              'TG_NB_TFIDF'] 
                              
            queryset = Algorithm.objects.using(database).filter(
                name__in = algorithm_list     
            )
            
            comments_score_query = """
                SELECT newsitem.id nid, comment.id, result.value
                  FROM newsitem, comment, text, result
                 WHERE comment.NewsItemID = newsitem.id
                   AND comment.text_id = text.id
                   AND text.id = result.text_id
                   AND result.algorithm_id = %s      
                 ORDER BY nid, value
            """             
            
            insert_summary_query = """
                INSERT INTO `newsitem_pos_neg_comments`(`newsitem_id`, 
                                                        `algorithm_id`,
                                                        `pos_comments`,
                                                        `neg_comments`,
                                                        `neutral_comments`) 
                VALUES (%s,%s,%s,%s,%s)
            """
            
            insert_detail_query = """
                INSERT INTO `pos_neg_comments`(`algorithm_id`,
                                               `newsitem_id`, 
                                               `comment_id`,
                                               `sentiment`) 
                VALUES (%s,%s,%s,%s)
            """            
            
            cursor = connections[database].cursor()
            
            for algorithm in queryset_iterator(queryset, chunksize=1000):
                
                print "Processing algorithm {}".format(algorithm.name)
                
                cursor.execute(comments_score_query, [algorithm.id])
                
                current_newsitem = 0
                type_hash = Counter({POSITIVE_COMMENT: 0,
                                     NEGATIVE_COMMENT: 0,
                                     NEUTRAL_COMMENT: 0})
            
                with transaction.atomic():
                    self.pbar_setup(maxval=cursor.rowcount)
                    insert_cursor = connections[database].cursor()
                    detail_rows_to_insert = []
                    summary_rows_to_insert = []
                    for row in dictfetch(cursor):
                       
                        if row['nid'] != current_newsitem:
                            if current_newsitem > 0:
                                summary_rows_to_insert.append([
                                    current_newsitem,
                                    algorithm.id,
                                    type_hash[POSITIVE_COMMENT],
                                    type_hash[NEGATIVE_COMMENT],
                                    type_hash[NEUTRAL_COMMENT],
                                ])
                            current_newsitem = row['nid']
                            type_hash = Counter({POSITIVE_COMMENT: 0,
                                                 NEGATIVE_COMMENT: 0,
                                                 NEUTRAL_COMMENT: 0})
                        else:
                            comment_type = self.check_result(algorithm, 
                                                             row['value'])
                            type_hash[comment_type] += 1
                            detail_rows_to_insert.append([
                                algorithm.id,
                                row['nid'],
                                row['id'],
                                comment_type
                            ])
                            if len(detail_rows_to_insert) >= 10000:
                                insert_cursor.executemany(insert_detail_query, 
                                                          detail_rows_to_insert)
                                detail_rows_to_insert = []
                    
                        self.pbar_increment()
                    if current_newsitem > 0:
                        summary_rows_to_insert.append([
                            current_newsitem,
                            algorithm.id,
                            type_hash[POSITIVE_COMMENT],
                            type_hash[NEGATIVE_COMMENT],
                            type_hash[NEUTRAL_COMMENT],
                        ])  
                    insert_cursor.executemany(insert_summary_query, 
                                              summary_rows_to_insert) 
                    self.pbar_destroy()                  
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
           
