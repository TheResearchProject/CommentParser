import datetime
import time
import pprint
import re

from django.core.management.base import CommandError
from django.db import transaction
from django.utils.dateparse import parse_datetime

import feedparser
import requests
from bs4 import BeautifulSoup     

from comment_parser.queryset_iterator import queryset_iterator

from rss_parser.models import *      

from rss_parser.mycommand import MyCommand

from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

class Command(MyCommand):
    help = 'Grabs the comments from each news from TheGuardian news RSS'
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        queryset = Newsitem.objects.all()
        
        self.pbar_setup(maxval=queryset.count())
        
        for newsitem in queryset_iterator(queryset, chunksize=10):
            
            shortId = newsitem.url.split('/')[-1]
            
            current_page = 1
            while True:
                resp = requests.get("https://api.nextgen.guardianapps.co.uk/discussion/p/{0}.json".format(shortId),{
                        'page': current_page,
                        'orderBy': 'oldest',
                        'pageSize': 100,
                        'displayThreaded': 'true',
                        'maxResponses': 1000000
                })
                if resp.status_code == 404:
                    break
                try:
                    dejson = resp.json()
                    comment_soup = BeautifulSoup(dejson['commentsHtml'], "html.parser")
                except MemoryError:
                    print "MemoryError when dealing with URL " + newsitem.url
                
                with transaction.atomic():
                    self.process_comment_ul(comment_soup.ul, newsitem, parent=None)
                
                current_page += 1
                if current_page > dejson['lastPage']:
                    break
                    
            self.pbar_increment()
        self.pbar_destroy()
                
                
    def process_comment_ul(self, ul_object, newsitem, parent=None):                
                
        for comment_li in ul_object.find_all('li', recursive=False):
            permalink = comment_li.find('a', 'd-comment__timestamp')['href']
            comment_id = 'theguardian-permalink-'+permalink.split('/')[-1]
            comment, created = Comment.objects.get_or_create(
                id=comment_id)
            comment.newsitem = newsitem
            comment.save()
            
            if created:
                comment.authorid = comment_li['data-comment-author']
                text = comment_li.find('div', 'd-comment__body').text.strip()
                comment.text = Text.objects.create(
                    text=text,
                    wordcount=len(tokenizer.tokenize(text)))
                
                score_element = comment_li.find('span','d-comment__recommend-count--new')
                comment.score = int(score_element.text) if score_element else 0
                
                #Removing the last ':' character. Example:
                #-Before: 2016-05-31T23:24:10.000+01:00
                #-After : 2016-05-31T23:24:10.000+0100
                time_text = comment_li['data-comment-timestamp']
                comment.date = parse_datetime(time_text[:-3]+time_text[-2:])
                
                if parent:
                    comment.parent = parent
                    
                comment.save()
            
            sub_comment_list = comment_li.ul
            if sub_comment_list:
                self.process_comment_ul(sub_comment_list, newsitem, parent=comment)        