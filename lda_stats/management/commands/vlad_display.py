import os
import time

import pdb

from django.core.management.base import BaseCommand, CommandError

from gensim.models import LdaModel
from gensim import corpora

from rss_parser.models import Word, Comment

class Command(BaseCommand):
    help = 'Calculate the hot topics'
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        dictionary_path = "models/dictionary.dict"
        corpus_path = "models/corpus.lda-c"
        lda_num_topics = 50
        lda_model_path = "models/lda_model_50_topics.lda"
        
        dictionary = corpora.Dictionary.load(dictionary_path)
        corpus = corpora.BleiCorpus(corpus_path)
        lda = LdaModel.load(lda_model_path)
        
        i = 0
        for topic in lda.show_topics(num_topics=lda_num_topics):
            print '#' + str(i) + ': ' + str(topic)
            i += 1
        
