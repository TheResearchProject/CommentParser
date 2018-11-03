import json

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Max, Min

from rss_parser.models import ExtraSettings, Newsitem
from rss_parser.mycommand import MyCommand

from lda_stats.algorithms import tfidf

class Command(MyCommand):
    help = 'Calculate the hot topics'
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        for database in self.selected_dbs:
        
            print "Calculating influential words for database " + database
        
            result = Newsitem.objects.using(database)\
                                     .annotate(num_comments=Count('comment'))\
                                     .order_by('-num_comments')[:25]    
                                     
            tfidf_array = tfidf.getTFIDFArray([ni.text.text for ni in result])
            
            top_words = []
            for w in sorted(tfidf_array, key=tfidf_array.get, reverse=True)[:20]:
                top_words.append({"word": w, "score": int(tfidf_array[w])})
                
            obj, created = ExtraSettings.objects.using(database).get_or_create(
                setting_name = 'influential_tfidf')    
            obj.setting_value = json.dumps(top_words)
            obj.save()
            
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
