import re

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import requests
from bs4 import BeautifulSoup

from rss_parser.mycommand import MyCommand
    
from comment_parser.queryset_iterator import queryset_iterator    

from rss_parser.models import Newsitem, Topic

class Command(MyCommand):
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        queryset = Newsitem.objects.filter(topics__isnull=True)
        
        self.pbar_setup(maxval=queryset.count())
        
        done = 0
        
        for newsitem in queryset_iterator(queryset):
            try:
                resp = requests.get(newsitem.url)
                soup = BeautifulSoup(resp.text, "html.parser")
                for meta in soup('meta'):
                    attrs = meta.__dict__['attrs']
                    if 'property' in attrs and attrs['property'] == 'article:tag':
                        with transaction.atomic():
                            for topic_name in attrs['content'].split(','):
                                topic, created = Topic.objects.get_or_create(
                                    name=topic_name)
                                newsitem.topics.add(topic)
                            newsitem.save()
                        break
            except Exception as e:
                print "Error processing URL: {0} -=- message: {1}".format(
                    newsitem.url, e)
            
            self.pbar_increment()
            
        self.pbar_destroy()
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))            