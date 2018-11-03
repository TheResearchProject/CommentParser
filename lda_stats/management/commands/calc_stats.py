import pdb

from django.core.management.base import BaseCommand, CommandError
from django.db import connections

from rss_parser.models import GeneralStats
from rss_parser.mycommand import MyCommand

class Command(MyCommand):
    help = 'Calculate the statistics'
    
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--list_stats', action='store_true', 
                                            default=False,
                                            help="Lists available stats calculations.")
        
        parser.add_argument('--stat', default="",
                                      help="Calculate only a specific stat.")         
          
    def calc_stat(self, database, stat, query):
        cursor = connections[database].cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        stat_obj, created = GeneralStats.objects.using(database)\
                                        .get_or_create(stat_name=stat)
        stat_obj.stat_value = result[0]
        stat_obj.save()        
          
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        stats_dic = {
            "start_date": "select min(Date) as stat from newsitem",
            "newsitems_num": "select count(*) as stat from newsitem",
            "authors_num": "select count(distinct author_id) as stat from author_newsitem",
            "comments_num": "select count(*) as stat from comment",
            "commenters_num": "select count(distinct AuthorID) as stat from comment",
            "newsitem_author_avg": "select floor(count(*)/count(distinct author_id)) as stat from author_newsitem",
            "comment_commenter_avg": "select floor(count(*)/count(distinct AuthorID)) as stat from comment",
            "images_num": "select count(*) as stat from images",
            "images_newsitem_avg": "select floor(count(*)/count(distinct newsitemId)) as stat from images",
            "socialnet_num": "select sum(Twitter+Facebook+GooglePlus+PinIt) as stat from newsitem;",
            "socialnet_avg": "select avg(Twitter+Facebook+GooglePlus+PinIt) as stat from newsitem;",
            "comment_newsitem_avg": "select floor(count(*)/count(distinct newsitemID)) as stat from comment",
            "newsitem_words_avg": "SELECT floor(avg(LENGTH(Content) - LENGTH(REPLACE(Content, ' ', '')) + 1)) as stat from newsitem",
            "comment_words_avg": "SELECT floor(avg(LENGTH(Content) - LENGTH(REPLACE(Content, ' ', '')) + 1)) as stat from comment",
            "newsitem_wordlen_avg": "SELECT avg(LENGTH(Content) / (LENGTH(Content) - LENGTH(REPLACE(Content, ' ', '')) + 1)) as stat from newsitem",
            "comment_wordlen_avg": "SELECT avg(LENGTH(Content) / (LENGTH(Content) - LENGTH(REPLACE(Content, ' ', '')) + 1)) as stat from newsitem",
            "comment_length_avg": "SELECT avg(LENGTH(Content)) as stat from comment",
            "comment_score_avg": "SELECT avg(score) stat FROM `comment`",
            "first_newsitem": "SELECT MIN(date) stat FROM newsitem",
            "last_newsitem": "SELECT MAX(date) stat FROM newsitem",
        }   
        
        if options['list_stats']:
            self.stdout.write("=== Available stats ===")
            for stat in stats_dic.keys():
                self.stdout.write(stat)
            return
            
        if options['stat'] and options['stat'] not in stats_dic:
            self.stdout.write(self.style.ERROR(
                'Stat {} not available'.format(options['stat'])))
            return
        
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            
            if options['stat'] != "":
                self.calc_stat(database=database, 
                               stat=options['stat'], 
                               query=stats_dic[options['stat']])
            else:
                for stat, query in stats_dic.iteritems():
                    self.calc_stat(database, stat, query)
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
           
