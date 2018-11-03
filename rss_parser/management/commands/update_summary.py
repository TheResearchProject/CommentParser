import pdb

from rss_parser.mycommand import MyCommand

from rss_parser.models import Newsitem

from comment_parser.queryset_iterator import queryset_iterator
from comment_parser.multi_db_iterator import MultiDbIterator

from gensim.summarization import summarize

class Command(MyCommand):
    help = 'Calculate the hot topics'
    items_used = "*"
    
    def handle(self, *args, **options):        
        self.stdout.write('Command started') 
        super(Command, self).handle(self, *args, **options)
        
        multi_db_iterator = MultiDbIterator(Newsitem)
        
        self.stdout.write('Sending queries to the databases, this might take a while...')
        multi_db_iterator.query(filters={
            'text__text__isnull': False,       
            'text__isnull': False,                
            'text__summary__isnull': True,       
        })
        
        if multi_db_iterator.total_count == 0:
            self.stdout.write("No newsitems need summarization!")
            return
        
        failed = 0
        
        self.pbar_setup(maxval=multi_db_iterator.total_count)      
        
        for newsitem in multi_db_iterator.get_iterator():

            try:
                newsitem.text.summary = summarize(newsitem.text.text)
            except:
                failed += 1
            newsitem.text.save()
            
            self.pbar_increment()    
            
        self.pbar_destroy()
        
        if failed > 0:
            self.stdout.write(self.style.WARNING('{} texts could not be summarized.'))        
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
