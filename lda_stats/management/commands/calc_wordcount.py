import HTMLParser
import re

from django.db import transaction

from rss_parser.models import Text
from rss_parser.mycommand import MyCommand
from comment_parser.queryset_iterator import queryset_iterator

from bulk_update.helper import bulk_update

class Command(MyCommand):
    help = 'Calculate the statistics'
    
    def clean_text(self, text):
        text = self.html_parser.unescape(text)
        text = re.sub('@[\w_]+','',text)
        text = re.sub('(https?://[\w\.\/\?&=]+)\s?','',text)
        text = re.sub('[^\w\s#_\']',' ',text)
        text = re.sub('\s{2,9999}',' ',text)
        return text.lower()        
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        self.html_parser = HTMLParser.HTMLParser()
        
        for db_name in self.selected_dbs:
            print "Calculating wordcount for database " + db_name        
            queryset = Text.objects.using(db_name).all()
            
            with transaction.atomic():

                self.pbar_setup(maxval=queryset.count())
                for text in queryset_iterator(queryset, chunksize=10000):
                
                    wordcount = len(self.clean_text(text.text).split())
                    
                    text.wordcount = wordcount
                    text.save()
                    
                    self.pbar_increment()
            
                self.pbar_destroy()  
            
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
           
