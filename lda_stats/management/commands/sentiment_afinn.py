import copy
from multiprocessing import Pool, Process

from rss_parser.mycommand import MyCommand
from rss_parser.models import Algorithm, Result, Text

from django.db import connections

from comment_parser.queryset_iterator import queryset_iterator

from afinn import Afinn

afinn = Afinn()

def bulk_create(database, results):
    Result.objects.using(database).bulk_create(results)

def afinn_score(text):
    return text, afinn.score(text.text)

class Command(MyCommand):
    help = 'Calculate the hot topics'
    algorithm_name = 'afinn'
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        filters = {}
        if options['only_newsitems']:
            filters['newsitem__isnull'] = False
        elif options['only_comments']:
            filters['comment__isnull'] = False
            
        for database in self.selected_dbs:    
            
            print "Processing database " + database
            
            algorithm, created = Algorithm.objects.using(database)\
                                        .get_or_create(name=self.algorithm_name)

            print "Removing previous results"      
            query = """
            DELETE FROM result WHERE algorithm_id IN (
                SELECT id
                  FROM algorithm 
                 WHERE name = %s
            )"""            
            cursor = connections[database].cursor()
            cursor.execute(query, [self.algorithm_name])

            print "Querying database"
            queryset = Text.objects.using(database).filter(**filters)
            
            results = []
            
            print "Calculating..."
            self.pbar_setup(maxval=queryset.count())
            queryset_iter = queryset_iterator(queryset, chunksize=2000)
    
            bulk_create_process = None
            pool = Pool()
            
            for text, result in pool.imap_unordered(afinn_score, queryset_iter):
                results.append(Result(algorithm=algorithm,
                                      text=text,
                                      value=str(result)))
                self.pbar_increment()
                
                if len(results) >= 10000:
                    if bulk_create_process and bulk_create_process.is_alive():
                        bulk_create_process.join()
                    bulk_create_process = Process(
                        target=bulk_create,
                        kwargs={'database': database,
                                'results': copy.copy(results)}
                    )
                    bulk_create_process.start()
                    results = []
    
            self.pbar_destroy()       
            
            print "Saving results"
            if bulk_create_process and bulk_create_process.is_alive():
                bulk_create_process.join()
            Result.objects.using(database).bulk_create(results)
            
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))