import datetime
import time
import pdb
import re

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_datetime
from django.db.models import Q

import feedparser
import requests
from bs4 import BeautifulSoup

from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
        
from comment_parser.queryset_iterator import queryset_iterator    

from rss_parser.models import *

class Command(BaseCommand):
    help = 'Updates data from TheGuardian news RSS and grabs the comments from each news'
    
    def add_arguments(self, parser):
        parser.add_argument('--check-missing', action='store_true')    
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        if options['check_missing']:
            self.check_items()
        else:
            self.parse_feed("http://www.theguardian.com/uk/media/rss")
                
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
        
    def parse_feed(self, feed_url):
        feed = feedparser.parse( feed_url )
        
        for item in feed['items']:
            if item['id'].startswith("https://www.theguardian.com/media/video"):
                continue
            self.stdout.write("Parsing url: "+item['id'])
            
            try:
                soup = BeautifulSoup(requests.get(item['id']).text, "html.parser")
            except requests.exceptions.TooManyRedirects:
                self.stdout.write("Skipping due to too many redirects")
                continue
            except requests.exceptions.ConnectionError:
                self.stdout.write("Connection error. Skipping")
                continue
                
            somedata = soup.find('script',id='gu')
            match = re.search('"shortUrl":"(.+)","thumbnail"', somedata.text)
            shorturl = match.group(1)
            
            newsitem, created = Newsitem.objects.get_or_create(
                url = shorturl
            )
            
            newsitem_ok = True
            
            if created:
                self.update_news_info(newsitem, soup) 
            newsitem.facebook = self.get_facebook_shares(item['id']) + self.get_facebook_shares(shorturl)
            
            newsitem.save()  
            
    def check_items(self):
        queryset = Newsitem.objects.filter(Q(lead="")|
                                           Q(text__isnull=True)|
                                           Q(title="")|
                                           Q(date__isnull=True)|
                                           Q(idauthor=""))
        
        for newsitem in queryset_iterator(queryset, chunksize=100):
            self.stdout.write("Processing URL "+newsitem.url)
            soup = BeautifulSoup(requests.get(newsitem.url).text, "html.parser")
            self.update_news_info(newsitem, soup)
            newsitem.save()
            
    def update_news_info(self, newsitem, soup):
        article_lead = soup.find('meta', itemprop='description')
        if article_lead:
            newsitem.lead  = article_lead['content']
        else:
            self.stdout.write("Article has no lead!")
        article_body = soup.find('div', itemprop='articleBody')
        if article_body:
            newsitem.text = Text.objects.create(
                text=article_body.text,
                wordcount=len(tokenizer.tokenize(article_body.text)))
        else:
            self.stdout.write("Article body not found!")
        article_title = soup.find('h1', 'content__headline')
        if article_title:
            newsitem.title = article_title.text.strip()
        else:
            self.stdout.write("Title not found!")
        date_published = soup.find('time', itemprop="datePublished")
        newsitem.date = date_published['datetime']
        author = soup.find('a', rel="author")
        if author:
            newsitem.idauthor = author.text
        else:
            self.stdout.write("Author not found!")
        
                            
    def get_facebook_shares(self, url):
        resp = requests.get("https://graph.facebook.com/" + url)
        dejson = resp.json()
        return dejson['shares'] if 'shares' in dejson else 0
        
