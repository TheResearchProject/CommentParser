from datetime import timedelta
import pdb
import pprint
import sys

from django.db.models import Max, Min

import nltk

from lda_stats.utils.vocabulary import Vocabulary
from lda_stats.utils.lda import LDA, lda_learning
from lda_stats.utils.stopwords import Stopwords
from lda_stats.utils.rake import Rake

from rss_parser.models import HotTopics, Newsitem
from rss_parser.mycommand import MyCommand
from comment_parser.queryset_iterator import queryset_iterator

class Command(MyCommand):
    help = 'Calculate the hot topics'
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        for db_name in self.selected_dbs:
            print "Calculating hot topics for database " + db_name
        
            dates = Newsitem.objects.using(db_name)\
                                    .all()\
                                    .aggregate(Min('date'),Max('date'))
                                              
            self.stdout.write("Start date: {0} -=- End date: {1}"\
                       .format(dates['date__min'], dates['date__max']))
            
            #{algorithm_name: algorithm_funtion}
            algs = {
                "lda_phrases": self.lda_phrases,
                "lda": self.lda_regular,
            }
            
            #pdb.set_trace()
        
            print "Removing previous resuls"
            HotTopics.objects.using(db_name).all().delete()
            
            for alg in algs.keys():
                for period in [1,3,12]:
                    self.save_hottopics(alg, 
                                        algs[alg], 
                                        period, 
                                        dates['date__min'], 
                                        dates['date__max'],
                                        db_name)        
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
        
    def save_hottopics(self, alg_name, alg_function, period, start_date, end_date, database):
        # Remove current records from table
        start = start_date
        while start <= end_date:
            end = start + timedelta(days=period*30)
            self.stdout.write("start: {0} -=- end {1}".format(start, end))
            topics = alg_function(date_to=end, 
                                  date_from=start, 
                                  num_topics=1,
                                  table="Newsitem",
                                  database=database)
            
            if topics:
                topics_str = ",".join([t[0] for t in topics[0][:10]])
                HotTopics.objects.using(database).create(
                    topics = topics_str,
                    algorithm = alg_name,
                    period = period)
            start = end+timedelta(days=1)        
            
    def lda_regular(self, *args, **kwargs):
        return self.lda(*args, **kwargs)
        
    def lda_phrases(self, *args, **kwargs):
        return self.lda(*args, phrase=True, **kwargs)
            
    def lda(self, database,
                  table="Comment", 
                  date_to=None, 
                  date_from=None, 
                  num_topics=10, 
                  alpha=0.5,
                  beta=0.5,
                  iteration_count=25,
                  smart_init=False,
                  phrase=False):
    
        model = self.str_to_class(table)
        items = model.objects.using(database).exclude(text__isnull=True)\
                                             .filter(date__gte=date_from,
                                                     date__lte=date_to)\
                                             .only('text')
                             
        if items.count() == 0:
            return []
                             
        contents = [i.text.text for i in items]   
        
        all_docs = []
        if phrase:
            for i in queryset_iterator(items, chunksize=100):
                rake = Rake('stopwords.txt')
                keywords = rake.run(i.text.text)
                all_docs.append([k[0] for k in keywords if " " in k[0]])            
        else:
            for i in queryset_iterator(items, chunksize=100):
                tokenized = nltk.word_tokenize(i.text.text.encode("ascii", "ignore"))
                all_docs.append(tokenized)            
        
        stopwords = Stopwords('stopwords.txt')
        voca = Vocabulary(stopwords, excluds_stopwords=True)
        docs = [voca.doc_to_ids(doc) for doc in all_docs]
        
        lda = LDA(num_topics, alpha, beta, docs, voca.size(), smart_init)
        
        topics = lda_learning(lda, iteration_count, voca)
        
        return topics
        
    def str_to_class(self, str): 
        return getattr(sys.modules[__name__], str)      
        