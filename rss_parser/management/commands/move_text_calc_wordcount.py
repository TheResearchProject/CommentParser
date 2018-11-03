import itertools
import pdb

from django.db import transaction

from nltk.tokenize import RegexpTokenizer

from rss_parser.mycommand import MyCommand

from rss_parser.models import Newsitem, Comment, Text

from comment_parser.queryset_iterator import queryset_iterator
from comment_parser.multi_db_iterator import MultiDbIterator

from gensim.summarization import summarize

class Command(MyCommand):
    help = 'Calculate the hot topics'
    items_used = "*"
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        if len(self.selected_dbs) > 1:
            self.stdout.write(self.style.ERROR('You must choose a specific DB for this command'))
            return
        
        database = self.selected_dbs[0]
        
        current_text_id = 560000
        
        for model in ['Newsitem']:
            queryset = globals()[model].objects.using(database).filter(text__isnull=True)
            if queryset.count() == 0:
                continue
                
            text_list = []    
            item_list = []
                
            print "Processing " + model
            self.pbar_setup(maxval=queryset.count())     
            tokenizer = RegexpTokenizer(r'\w+')
            for item in queryset_iterator(queryset, chunksize=1000):
                if item.content:
                    current_text = Text(
                        id=current_text_id,
                        text=item.content,
                        wordcount=len(tokenizer.tokenize(item.content)))
                    text_list.append(current_text)
                    item.text = current_text
                    item_list.append(item)
                    current_text_id += 1
                self.pbar_increment()
                
                if len(text_list) >= 2000:
                    Text.objects.using(database).bulk_create(text_list)
                    with transaction.atomic(database):
                        for (item, text) in itertools.izip(item_list, text_list):
                            item.text = text
                            item.save()
                    item_list = []
                    text_list = []
                
            self.pbar_destroy()
            
            print "Saving final results..."
            Text.objects.using(database).bulk_create(text_list)
            with transaction.atomic(database):
                for (item, text) in itertools.izip(item_list, text_list):
                    item.text = text
                    item.save()
            
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
