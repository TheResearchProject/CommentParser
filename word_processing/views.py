from collections import Counter
import datetime
from decimal import *
import math
import os
import pprint
import pdb

from django.db import connections
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

import requests
from bs4 import UnicodeDammit, BeautifulSoup

from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer

from pattern.en import lemma as lemmatizer_en
from pattern.nl import lemma as lemmatizer_nl

import numpy

from rss_parser.models import Comment, Newsitem

import obo
from text_parser import TextProcessor

text_processor = TextProcessor()    

re_vowel_en = re.compile("[aAeEiIoOuU]")
re_vowel_nl = re.compile("IJ|ij|[aAeEiIoOuU]")

# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'word_processing/index.html')
        
    def post(self, request):
        
        pprint.pprint(request.POST)
        pprint.pprint(request.FILES)
        
        #Language check
        if request.POST['language'] not in ['english', 'dutch']:
            return jsonify(status='error', message="Invalid language!")
            
        if request.POST['database'] not in connections:
            return jsonify(status='error', message="Invalid database!")
        
        #Input normalization
        if request.POST['upload_option'] == 'text_field':
            input_text = request.POST['upload_textarea']
        elif request.POST['upload_option'] == 'url':
            page_text = requests.get(request.POST['upload_url']).text
            soup = BeautifulSoup(page_text, "html.parser")
            input_text = soup.text
        elif request.POST['upload_option'] == 'file':
            input_text = UnicodeDammit(request.FILES['upload_file'].read()).unicode_markup
        elif request.POST['upload_option'] == 'news_comments':
            start_date_text = request.POST['news_comments_start_date']
            end_date_text = request.POST['news_comments_end_date']
            start_date = datetime.date(*[int(i) for i in start_date_text.split('-')])
            end_date = datetime.date(*[int(i) for i in end_date_text.split('-')])
            filters = {
                'date__gte': start_date,   
                'date__lte': end_date,
                'text__isnull': False
            }
            input_text = ""
            if 'news' in request.POST['news_comments']:
                queryset = Newsitem.objects\
                                   .using(request.POST['database'])\
                                   .filter(**filters)\
                                   .select_related('text')
                for newsitem in queryset:
                    input_text += "\n"+newsitem.text.text
            if 'comments' in request.POST['news_comments']:
                for comment in Comment.objects\
                                      .using(request.POST['database'])\
                                      .filter(**filters)\
                                      .select_related('text'):
                    input_text += "\n"+comment.text.text            
        #Stemmer selection
        if request.POST['stemmer'] == 'no_stemmer':
            stemmer = None
        elif request.POST['stemmer'] == 'porter':
            if request.POST['language'] != 'english':
                return jsonify(status='error', message="Invalid language for stemmer porter!")
            stemmer = PorterStemmer()
        elif request.POST['stemmer'] == 'snowball':
            stemmer = SnowballStemmer(request.POST['language'])
        else:
            return jsonify(status='error', message="Invalid stemmer!")
                
        #Lemmatizer selection
        if request.POST['lemmatizer'] == 'lemmatizer_off':
            lemmatizer = None
        elif request.POST['language'] == 'english':
            lemmatizer = lemmatizer_en
        else:
            lemmatizer = lemmatizer_nl
            
        #Stopwords selection    
        if request.POST['stopwords'] == 'no_stopwords':    
            stopwords = None
        elif request.POST['stopwords'] == 'our_stopwords':
            stopwords = obo.stopwords
        elif request.POST['stopwords'] == 'custom_stopwords':
            custom_stopword_text = UnicodeDammit(request.FILES.get('custom_stopword_file').read()).unicode_markup
            stopwords = obo.stripNonAlphaNum(custom_stopword_text)
            
        #Process the text  
        input_text_word_count = 0
        resulting_text = ""
        final_wordlist = []
        for word_type, word in text_processor.parse_text(input_text):
            if word_type == "non-word":
                resulting_text += word
            else:
                input_text_word_count += 1
                processed_word = word
                if stemmer:
                    processed_word = stemmer.stem(processed_word)
                if lemmatizer:
                    processed_word = lemmatizer(processed_word)
                if not stopwords or processed_word not in stopwords:
                    if request.POST['exclude_vowels'] == 'exclude_vowels_yes':
                        if request.POST['language'] == 'english':
                            regex = re_vowel_en
                        else:
                            regex = re_vowel_nl
                        processed_word = regex.sub("", processed_word)
                    resulting_text += processed_word
                    final_wordlist.append(processed_word)
          
        dictionary = obo.wordListToFreqDict(final_wordlist)
        sorteddict = obo.sortFreqDict(dictionary)   
          
        ignore_results_amount = int(request.POST['ignore_results_amount'])  
          
        if ignore_results_amount > 0:
            initial_index = ignore_results_amount
            ignored_words = [word for rank, word in sorteddict[:initial_index]]
            sorteddict = sorteddict[initial_index:]    
            new_text = ""
            new_wordlist = []
            for word_type, word in text_processor.parse_text(resulting_text):
                if word_type == "non-word":
                    new_text += word
                elif word not in ignored_words:
                    new_text += word
                    new_wordlist.append(word)
            resulting_text = new_text
            final_wordlist = new_wordlist
                    
        else:
            initial_index = 0          
          
        #Do the math!    
        input_text_char_count = len(input_text)
        word_count = len(final_wordlist)    
        distinct_words_count = len(sorteddict)
        words = []
        frequencies = []
        word_cloud = []
        for frequency, word in sorteddict:
            words.append(word)
            frequencies.append(frequency)
            word_cloud.append([word, frequency])

        acum_perc = Decimal(0)
        percentages = []
        acum_perc_list = []
        for freq in frequencies:
            perc = Decimal((freq*100.0)/word_count)
            percentages.append(round(perc, 2))
            acum_perc += perc
            acum_perc_list.append(round(acum_perc, 2))
            
            
        logarithms = []    
        for i in range(len(sorteddict)):    
            logarithms.append((math.log(i+1), math.log(frequencies[i])))
            
        #Calculate Linear regression
        #http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq
        x = numpy.array([math.log(f) for f in frequencies])
        y = numpy.array([math.log(rank) for rank in range(1, distinct_words_count + 1)])
        A = numpy.vstack([x, numpy.ones(len(x))]).T
        m, c = numpy.linalg.lstsq(A, y)[0]
        
        #Calculate the regression line start and end, 
        #  and sort making the start be the one with the lower X value
        #  (highcharts requires this)
        regline_start = (0, c)
        regline_end = (math.log(distinct_words_count), math.log(distinct_words_count) * m + c)
        regression_line = {
            'start': regline_start,
            'end': regline_end
        }
            
        return JsonResponse({
           'status': 'success', 
           'words': words,
           'frequencies': frequencies,
           'percentages': percentages,
           'acum_perc_list': acum_perc_list,
           'logarithms': logarithms,
           'regression_line': regression_line,
           'resulting_text': resulting_text,
           'input_text_char_count': input_text_char_count,
           'input_text_word_count': input_text_word_count,
           'output_text_word_count': word_count,
           'word_cloud': word_cloud,
           'sorteddict': sorteddict
        })        