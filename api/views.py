import cPickle
from collections import Counter, OrderedDict
import datetime
from decimal import Decimal
import itertools
import json
import math
import os
import pprint
import pdb
import random
import re
import time

from django.conf import settings
from django.db import connections
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import View

from celery.result import AsyncResult
from celery.exceptions import TaskRevokedError

from bs4 import UnicodeDammit, BeautifulSoup
import MySQLdb
import requests

from gensim.models.word2vec import Word2Vec
import numpy
from scipy.stats import mannwhitneyu, wilcoxon, pearsonr
from scipy.stats.mstats import spearmanr
from sklearn.manifold import TSNE      

from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer

from pattern.en import lemma as lemmatizer_en
from pattern.nl import lemma as lemmatizer_nl

# From histwords module
from representations.embedding import Embedding

import networkx

from rss_parser.models import Algorithm,\
                              Cat1,\
                              Category,\
                              Comment,\
                              Newsitem,\
                              Result
from comment_parser.utils import dictfetch
import api.tasks
from comment_parser.celery import app as celery_app
from api.common import StatisticFunctions

import word_processing.obo as obo
from word_processing.text_parser import TextProcessor     

@require_http_methods(['POST'])
@csrf_exempt
def create_task(request):
    input_json = json.loads(request.body)
    print input_json
    
    task_name = input_json['task_name']
    parameters = input_json['parameters']
    
    try:
        res = getattr(api.tasks, task_name).delay(**parameters)
    except Exception as e:
        return JsonResponse({
            'status': 'failure',
            'task_id': None,
            'message': e.message
        }) 
         
    return JsonResponse({
        'status': 'success',
        'task_id': res.id,
        'message': ''
    })    
    
@require_http_methods(['POST'])
@csrf_exempt
def get_task_status(request):
    input_json = json.loads(request.body)   
    
    res = AsyncResult(input_json['task_id'], app=celery_app)
    
    response = {
        'state': res.state,
        'info': None,
        'message': ""
    }
    
    message = ""
    if getattr(res.info, 'message', None) and res.info.message == 'terminated':
        response['message'] = "Task was revoked/cancelled"
    else:
        response['info'] = res.info
        
    try:
        return JsonResponse(response)
    except TypeError:
        response['info'] = str(res.info)
        return JsonResponse(response)
    
@require_http_methods(['POST'])
@csrf_exempt
def kill_task(request):
    input_json = json.loads(request.body)   
    
    res = AsyncResult(input_json['task_id'], app=celery_app)
    res.revoke(terminate=True, signal="SIGKILL")
    
    return JsonResponse({
        'state': 'REVOKED',
        'info': None,
        'message': "Done!"
    })    

#   ____  _      _____    __  __ ______ _______ _    _  ____  _____   _____ 
#  / __ \| |    |  __ \  |  \/  |  ____|__   __| |  | |/ __ \|  __ \ / ____|
# | |  | | |    | |  | | | \  / | |__     | |  | |__| | |  | | |  | | (___  
# | |  | | |    | |  | | | |\/| |  __|    | |  |  __  | |  | | |  | |\___ \ 
# | |__| | |____| |__| | | |  | | |____   | |  | |  | | |__| | |__| |____) |
#  \____/|______|_____/  |_|  |_|______|  |_|  |_|  |_|\____/|_____/|_____/ 

models = {
    0:'Newsitems',
    1:'EnglishBooks-1800',
    2:'EnglishBooks-1810',
    3:'EnglishBooks-1820',             
    4:'EnglishBooks-1830',
    5:'EnglishBooks-1840',
    6:'EnglishBooks-1850',
    7:'EnglishBooks-1860',
    8:'EnglishBooks-1870',
    9:'EnglishBooks-1880',
    10:'EnglishBooks-1890',
    11:'EnglishBooks-1900',
    12:'EnglishBooks-1910',
    13:'EnglishBooks-1920',
    14:'EnglishBooks-1930',
    15:'EnglishBooks-1940',
    16:'EnglishBooks-1950',
    17:'EnglishBooks-1960',
    18:'EnglishBooks-1970',
    19:'EnglishBooks-1980',
    20:'EnglishBooks-1990',
}

class EnglishBooksModel():
    def __init__(self, model_code):
        model_name = models[model_code]
        year = model_name.split('-')[-1]
        self.embed = Embedding.load('files/sgns/'+year)
        self.embed.normalize()             
        
    def __getitem__(self, key):
        return self.embed.represent(key)
       
    def __contains__(self, k):
        return self.has_key(k)
       
    def has_key(self, k):
        return self.embed.__contains__(k)        
        
    def most_similar(self, word):
        result = []
        for coef, word in self.embed.closest(word):
            if coef > 0:
                result.append((word, coef))
        return result
                                               
# Create your views here.
def available_models(request):               
    return JsonResponse({'models': models})

@require_http_methods(['POST'])
@csrf_exempt
def calculate_vectors(request):
    input_json = json.loads(request.body)   
    
    list_of_vectors = []
    messages = []
    
    model_code = int(input_json['model']) 
                                        
    if model_code == 0:
        model = Word2Vec.load('newsitems.word2vec')
    elif model_code >= 1 and model_code <= 20:
        model = EnglishBooksModel(model_code) 
        
    #Make sure the words are available in the model
    related_words = set()
    for word in input_json['words']:
        lower_word = word.lower()
        if lower_word not in model or sum(model[lower_word]) == 0:
            messages.append("Word {} not available in model.".format(word))
        else:
            related_words.add(lower_word)
    
    if len(related_words) > 0:
        #Get the related words
        for i in range(int(input_json['levels'])):
            next_level_related_words = set()
            for word in related_words:
                next_level_related_words.add(word)
                for related_word, _ in model.most_similar(word):
                    next_level_related_words.add(related_word)    
            related_words = next_level_related_words
            
        vectors = []
        for word in related_words:
            if word in model:
                vectors.append(model[word])
                
        tsne = TSNE(n_components=2, random_state=0)
        vectors2d = tsne.fit_transform(vectors)    
            
        for word, vector in itertools.izip(related_words, vectors2d):
            list_of_vectors.append({
                'x': vector[0]*1000,
                'y': vector[1]*1000,
                'title': word,
                'size': 20,
            })        
        
    return JsonResponse({'vectors': list_of_vectors,
                         'messages': messages})
    
#Build word vector for training set by using the average value of all word vectors in the tweet, then scale
def buildWordVector(text, size):
    vec = numpy.zeros(size).reshape((1, size))
    count = 0.
    for word in text:
        try:
            vec += w2v[word].reshape((1, size))
            count += 1.
        except KeyError:
            continue
    if count != 0:
        vec /= count
    return vec
    
class CsrfExemptView(View):    
    @method_decorator(csrf_exempt)   
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptView, self).dispatch(*args, **kwargs)      
    
class StatisticView(CsrfExemptView, StatisticFunctions):
    def get_months(self):
        cursor = connections[self.database].cursor()  
        sql = "SELECT DISTINCT MONTH(Date), YEAR(Date) FROM `newsitem` ORDER BY YEAR(Date), MONTH(Date) ASC"
        cursor.execute(sql)
        months = OrderedDict()
        for row in cursor.fetchall():
            month_string = "{}/{}".format(row[0], row[1])
            months[month_string] = month_string
        return months
        
    def get_categories(self):
        categories = Cat1.objects.using(self.database).all()
        category_dict = {}
        for cat in categories:
            category_dict[cat.id] = cat.label
        return category_dict
        
    def get_context(self):
        alg_data = {}
        
        query = """
            SELECT algorithm.id, 
                   algorithm.name, 
                   algorithm_nickname.nickname 
              FROM algorithm
            LEFT JOIN algorithm_nickname 
              ON algorithm.id = algorithm_nickname.algorithm_id
        """
        
        cursor = connections[self.database].cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            alg_data[row[0]] = row[2] if row[2] != None else row[1] 
            
        databases = {}    
        for db in settings.AVAILABLE_DATABASES:
            databases[db] = db
                    
        return {
            'selected_database':self.database,
            'databases':databases,
            'algorithms': alg_data
        }

    def get(self, request):
        self.set_database(request.GET)
        return JsonResponse(self.get_context())
            
class MannWhitneyUView(StatisticView):
    
    def get_context(self):
        context = super(MannWhitneyUView, self).get_context()    
        context['months'] = self.get_months()
        return context
        
    def post(self, request):
        input_json = json.loads(request.body)
        self.set_database(input_json['paramaters'])
        super(MannWhitneyUView, self).set_start_end_months(
            input_json['start_month'], input_json['end_month'])
        
        input_json = json.loads(request.body)  
        print input_json
        
        algorithm = Algorithm.objects.using(input_json['parameters']['database'])\
                                     .get(id=int(input_json['algorithm']))
        
        query = """
            SELECT newsitem_categories.category_id, result.value
              FROM newsitem, newsitem_categories, text, result
             WHERE newsitem.text_id = text.id
               AND text.id = result.text_id 
               AND newsitem.id = newsitem_categories.newsitem_id
               AND result.algorithm_id = %s 
               AND newsitem.date >= %s
               AND newsitem.date <= %s
        """
        
        cursor = connections[self.database].cursor()
        cursor.execute(query, [algorithm.id, self.start_date, self.end_date])
        
        newsitems_by_cat = {}
        for row in cursor.fetchall():
            cat1, value = row
            if not cat1 in newsitems_by_cat:
                newsitems_by_cat[cat1] = [Decimal(value)]
            else:
                newsitems_by_cat[cat1].append(Decimal(value))
                
        cat_keys = newsitems_by_cat.keys()
        cat_keys.sort()
        
        categories = Category.objects\
                             .using(self.database)\
                             .filter(id__in=cat_keys)
        cat_labels = [cat.label for cat in categories]

        category_data = []             
        results = []
        for cat1, cat_label in itertools.izip(cat_keys, cat_labels):
            cat_results = []
            for cat2 in cat_keys:
                try:
                    value = mannwhitneyu(x=newsitems_by_cat[cat1], 
                                         y=newsitems_by_cat[cat2])
                except Exception as e:
                    result = ("N/A","N/A")
                cat_results.append({
                    'testing_value': value[0],
                    'significance': value[1]
                })
            results.append({
                'name': cat_label,
                'results': cat_results,
                'amount_of_data': len(newsitems_by_cat[cat1])
            })
        
        return JsonResponse({'results': results})            

class WilcoxonMonthlyView(StatisticView):

    def get_context(self):
        context = super(WilcoxonMonthlyView, self).get_context()
        context['categories'] = self.get_categories()
        context['months'] = self.get_months()
        return context
        
    def post(self, request):
        input_json = json.loads(request.body)
        self.set_database(input_json)
        super(WilcoxonMonthlyView, self).set_start_end_months(
            input_json['start_month'], input_json['end_month'])
        
        input_json = json.loads(request.body)    
        
        context = self.get_context()
        
        category = Category.objects.using(self.database)\
                                   .get(id=input_json['category'])
                               
        context['category'] = category
                                                  
        algorithm = Algorithm.objects.using(self.database)\
                                     .get(id=input_json['algorithm'])
        context['selected_algorithm'] = algorithm
        
        query = """
            SELECT newsitem.date, result.value 
              FROM newsitem, newsitem_categories, text, result, algorithm
             WHERE newsitem.text_id = text.id
               AND result.text_id = text.id
               AND result.algorithm_id = algorithm.id      
               AND newsitem.id = newsitem_categories.newsitem_id
               AND algorithm.name = %s
               AND newsitem_categories.category_id = %s      
               AND newsitem.date >= %s
               AND newsitem.date <= %s               
        """
        
        cursor = connections[self.database].cursor()
        cursor.execute(query, [algorithm.name, 
                               category.id, 
                               self.start_date,
                               self.end_date])
        months = []
                    
        newsitems_by_month = {}
        for row in cursor.fetchall():
            month_year_key = "{}/{}".format(row[0].month, 
                                            row[0].year)
            if not month_year_key in newsitems_by_month:
                newsitems_by_month[month_year_key] = [Decimal(row[1])]
            else:
                newsitems_by_month[month_year_key].append(Decimal(row[1]))
                
        context['months_in_interval'] = newsitems_by_month.keys()
        
        headers = []        
        results = []
        for month1 in newsitems_by_month:
            headers.append({
                'month': month1,
                'amount_of_data': len(newsitems_by_month[month1])
            })
            month_results = []
            for month2 in newsitems_by_month:
                # Determine the month with the smaller amount of data
                min_data = min(len(newsitems_by_month[month1]),
                               len(newsitems_by_month[month2]))
                if min_data <= 1:
                    result = ("N/A", "N/A")
                else:
                    # Get the samples from each result
                    month1_sample = random.sample(newsitems_by_month[month1], min_data)
                    month2_sample = random.sample(newsitems_by_month[month2], min_data)
                    # Do the calculation
                    try:
                        result = wilcoxon(month1_sample, month2_sample)
                    except Exception as e:
                        result = ("N/A","N/A")
                month_results.append({
                    'testing_value': result[0],
                    'significance': result[1]
                })
            results.append({
                'month': month1,
                'amount_of_data': len(newsitems_by_month[month1]),
                'results': month_results
            })
        
        context['headers'] = headers
        context['results'] = results
        
        return JsonResponse({'headers': headers,
                             'results': results})    
        
class WilcoxonIntervalView(StatisticView):

    def get_context(self):
        context = super(WilcoxonIntervalView, self).get_context()
        context['categories'] = self.get_categories()
        return context
        
    def post(self, request):
        
        input_json = json.loads(request.body)
        print input_json
        
        self.set_database(input_json)
        
        context = self.get_context()
        
        mask = '%Y-%M-%d'
        
        context['start_date1'] = datetime.datetime.strptime(input_json['start_date1'], mask)
        context['start_date2'] = datetime.datetime.strptime(input_json['start_date2'], mask)
        context['end_date1'] =   datetime.datetime.strptime(input_json['end_date1']  , mask)
        context['end_date2'] =   datetime.datetime.strptime(input_json['end_date2']  , mask)
        
        category = Category.objects.using(self.database)\
                                   .get(id=input_json['category'])
        algorithm = Algorithm.objects.using(self.database)\
                                     .get(id=input_json['algorithm'])
        
        query = """
            SELECT result.value 
              FROM newsitem, newsitem_categories, text, result, algorithm
             WHERE newsitem.text_id = text.id
               AND result.text_id = text.id
               AND result.algorithm_id = algorithm.id
               AND newsitem.id = newsitem_categories.newsitem_id
               AND algorithm.name = %s
               AND newsitem_categories.category_id = %s     
               AND newsitem.date >= %s
               AND newsitem.date <= %s               
        """
        
        cursor = connections[self.database].cursor()      
        
        #Running query for interval 1
        cursor.execute(query, [algorithm.name, 
                               category.id, 
                               context['start_date1'],
                               context['end_date1']])
        results1 = [Decimal(row[0]) for row in cursor.fetchall()]     
        
        #Running query for interval 2
        cursor.execute(query, [algorithm.name, 
                               category.id, 
                               context['start_date2'],
                               context['end_date2']])
        results2 = [Decimal(row[0]) for row in cursor.fetchall()]     
        
        # Determine the month with the smaller amount of data
        min_data = min(len(results1), len(results2))
        if min_data <= 1:
            result = ("N/A", "N/A")
        else:
            # Get the samples from each result
            interval1_sample = random.sample(results1, min_data)
            interval2_sample = random.sample(results2, min_data)
            # Do the calculation
            try:
                result = wilcoxon(interval1_sample, interval2_sample)
            except Exception as e:
                result = ("N/A","N/A")
        
        return JsonResponse({'results': {'testing_value': result[0],
                                         'significance': result[1]}})   
        

text_processor = TextProcessor()    

re_vowel_en = re.compile("[aAeEiIoOuU]")
re_vowel_nl = re.compile("IJ|ij|[aAeEiIoOuU]")

# Create your views here.
class WordProcessingView(CsrfExemptView):
    def post(self, request):
        
        input_json = json.loads(request.body)
        
        #Language check
        if input_json['language'] not in ['english', 'dutch']:
            return jsonify(status='error', message="Invalid language!")
            
        if input_json['parameters']['database'] not in connections:
            return jsonify(status='error', message="Invalid database!")
        
        #Input normalization
        if input_json['upload_option'] == 'text_field':
            input_text = input_json['upload_textarea']
        elif input_json['upload_option'] == 'url':
            page_text = requests.get(input_json['upload_url']).text
            soup = BeautifulSoup(page_text, "html.parser")
            input_text = soup.text
        elif input_json['upload_option'] == 'file':
            input_text = UnicodeDammit(input_json['upload_file'].read()).unicode_markup
        elif input_json['upload_option'] == 'news_comments':
            start_date_text = input_json['news_comments_start_date']
            end_date_text = input_json['news_comments_end_date']
            start_date = datetime.date(*[int(i) for i in start_date_text.split('-')])
            end_date = datetime.date(*[int(i) for i in end_date_text.split('-')])
            filters = {
                'date__gte': start_date,   
                'date__lte': end_date,
                'text__isnull': False
            }
            input_text = ""
            if input_json['news_comments'] in ['news', 'news_comments']:
                queryset = Newsitem.objects\
                                   .using(input_json['parameters']['database'])\
                                   .filter(**filters)\
                                   .select_related('text')
                for newsitem in queryset:
                    input_text += "\n"+newsitem.text.text
            if input_json['news_comments'] in ['comments', 'news_comments']:
                for comment in Comment.objects\
                                      .using(input_json['parameters']['database'])\
                                      .filter(**filters)\
                                      .select_related('text'):
                    input_text += "\n"+comment.text.text            
        #Stemmer selection
        if input_json['stemmer'] == 'no_stemmer':
            stemmer = None
        elif input_json['stemmer'] == 'porter':
            if input_json['language'] != 'english':
                return jsonify(status='error', message="Invalid language for stemmer porter!")
            stemmer = PorterStemmer()
        elif input_json['stemmer'] == 'snowball':
            stemmer = SnowballStemmer(input_json['language'])
        else:
            return jsonify(status='error', message="Invalid stemmer!")
                
        #Lemmatizer selection
        if input_json['lemmatizer'] == 'lemmatizer_off':
            lemmatizer = None
        elif input_json['language'] == 'english':
            lemmatizer = lemmatizer_en
        else:
            lemmatizer = lemmatizer_nl
            
        #Stopwords selection    
        if input_json['stopwords'] == 'no_stopwords':    
            stopwords = None
        elif input_json['stopwords'] == 'our_stopwords':
            stopwords = obo.stopwords
        elif input_json['stopwords'] == 'custom_stopwords':
            custom_stopword_text = UnicodeDammit(input_json.get('custom_stopword_file').read()).unicode_markup
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
                    if input_json['exclude_vowels'] == 'exclude_vowels_yes':
                        if input_json['language'] == 'english':
                            regex = re_vowel_en
                        else:
                            regex = re_vowel_nl
                        processed_word = regex.sub("", processed_word)
                    resulting_text += processed_word
                    final_wordlist.append(processed_word)
          
        dictionary = obo.wordListToFreqDict(final_wordlist)
        sorteddict = obo.sortFreqDict(dictionary)   
          
        ignore_results_amount = int(input_json['ignore_results_amount'])  
          
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
        
def get_data(newsitem_id=None, 
             date_from=None, 
             date_to=None, 
             strip_by_date=False, 
             database=settings.AVAILABLE_DATABASES[0],
             algorithm=None):
    # init vars
    nodes=[]
    links=[]
    node_index={}     
    
    newsitem_ids = []
    
    #Running query for interval 1
    query = """
        SELECT newsitem.id
             ,newsitem.title 
             ,newsitem.idauthor 
             ,newsitem.date
             ,text.wordcount
             ,result.value 
             ,algorithm_color.color
          FROM algorithm_color, newsitem, text, result
         WHERE newsitem.text_id = text.id
           AND result.text_id = text.id
           AND result.algorithm_id = algorithm_color.algorithm_id
           AND result.value >= algorithm_color.min_threshold
           AND result.value < algorithm_color.max_threshold"""
    parameters = []

    if algorithm:
        parameters.append(int(algorithm))
        query += """
           AND result.algorithm_id = %s"""        

    if newsitem_id:
        parameters.append(int(newsitem_id))
        query += """
            AND newsitem.id = %s"""
    else:
        if date_from:
            parameters.append(date_from.date())
            query += """
                AND newsitem.date >= %s"""
        if date_to:
            parameters.append(date_to.date())
            query += """
                AND newsitem.date <= %s"""
    
    cursor = connections[database].cursor()  
    cursor.execute(query, parameters)
    
    for row in dictfetch(cursor):
        newsitem_ids.append(row['id'])
        node_index_key='N%d'%row['id']
        if node_index_key not in node_index:
            nodes.append({'type': 'n', 
                          'id': row['id'], 
                          'title': row['title'], 
                          'author': row['idauthor'], 
                          'date': row['date'], 
                          'wc': row['wordcount'],
                          'color': row['color']})
            node_index[node_index_key]=len(nodes)-1
        else:
            index = node_index[node_index_key]
            node = nodes[index]
            if row['idauthor']:
                node['author'] += ', ' + row['idauthor'] 
            
    query = """
        SELECT comment.id
             ,comment.authorid 
             ,comment.date
             ,comment.parentid
             ,comment.newsitemid
             ,text.wordcount
             ,result.value 
             ,algorithm_color.color
          FROM algorithm_color, comment, text, result
         WHERE comment.text_id = text.id
           AND result.text_id = text.id
           AND result.algorithm_id = algorithm_color.algorithm_id
           AND result.value >= algorithm_color.min_threshold
           AND result.value < algorithm_color.max_threshold"""
    parameters = []

    if algorithm:
        parameters.append(int(algorithm))
        query += """
           AND result.algorithm_id = %s"""

    if newsitem_id:
        parameters.append(int(newsitem_id))
        query += """
            AND newsitemid = %s"""
    else:
        if date_from:
            parameters.append(date_from.date())
            query += """
                AND comment.date >= %s"""
        if date_to:
            parameters.append(date_to.date())
            query += """
                AND comment.date <= %s"""
    
    #Running query for interval 1
    cursor.execute(query, parameters)
    comments = dictfetch(cursor)
    for row in comments:    
        nodes.append({'type': 'c', 
                      'id': row['id'], 
                      'title': "", 
                      'date': row['date'], 
                      'author': row['authorid'], 
                      'wc': row['wordcount'],
                      'color': row['color']})
        node_index['C%s'%row['id']]=len(nodes)-1
        
    cursor.execute(query, parameters)
    comments = dictfetch(cursor)        
    for comment in comments:  
        source=node_index['C%s'%comment['id']]
        if comment['parentid']:
            parent_node_id = '%s%s'%('C', comment['parentid'])
        else:
            parent_node_id = '%s%s'%('N', comment['newsitemid'])
        
        if parent_node_id in node_index:
            target=node_index[parent_node_id]
        elif '%s%s'%('N', comment['newsitemid']) in node_index:
            target=node_index['%s%s'%('N', comment['newsitemid'])]
        else:
            continue
            
        links.append({'source': source, 'target': target, 'date': comment['date']})
        
    return nodes, links
    
class NetvisDataView(StatisticView):
    def post(self, request):    
    
        input_json = json.loads(request.body)
    
        newsitem=input_json.get('newsitem', None)
        date_from_text = input_json.get('date_from', None)
        if date_from_text:
            date_from = datetime.datetime.strptime(date_from_text, '%d-%m-%Y')
        else:
            date_from = None
        date_to_text=input_json.get('date_to', None)
        if date_to_text:
            date_to = datetime.datetime.strptime(date_to_text, '%d-%m-%Y')
        else:
            date_to = None
        strip_by_date = True if input_json.get('strip_by_date') == 'true' else False
        if newsitem==None and (date_from==None or date_to==None):
            return json.dumps({'_type': 'error', 'message': 'invalid parameters'}) 
    
        nodes, links = get_data(newsitem_id=newsitem,
                                date_from=date_from, 
                                date_to=date_to,
                                algorithm=input_json['algorithm'],
                                database=input_json['parameters']['database'])
            
        return JsonResponse({'nodes': nodes, 'links': links})
    
class NetvisGraphInfoView(CsrfExemptView):
    def get(self, request):       
        # check params
        id1=request.GET.get('id1', None)
        if id1==None or len(id1)==0 or id1[0].lower() not in ('n', 'c'):
            return JsonResponse({'_type': 'error', 'message': 'invalid parameters'})
            
        database = request.GET.get('database')
    
        # retrieve id of newsitem
        id_type=id1[0].lower()
        id_val=int(id1[1:])    
        
        if id_type=='n':
            newsitem_id=id_val
        else:
            comment = Comment.objects.using(database).get(pk=id_val)
            if not comment:
                return JsonResponse({'_type': 'error', 'message': 'comment not fount'})
            newsitem_id = comment.newsitem_id
        
        nodes, links = get_data(newsitem_id=newsitem_id,
                                database=request.GET['database'],
                                algorithm=request.GET['algorithm_id'])
        
        if len(nodes)==0 or nodes[0]['type']!='n':
            return json.dumps({'_type': 'error', 'message': 'newsitem not found correctly'})
    
        # create networkx graph
        g=networkx.Graph()
        g.add_nodes_from(range(len(nodes)))
        g.add_edges_from([(i['source'], i['target']) for i in links])
    
        # find index of id1 in nodes
        ni=0 if id_type=='n' else map(lambda n: n['id'], nodes).index(id_val, 1)
        
        if g.number_of_edges()==0:
            diameter = 0
        else:
            diameter = networkx.diameter(g)
            
        # make result
        res={
            'newsitem': newsitem_id,
            'diameter': 0 if g.number_of_edges()==0 else networkx.diameter(g),
            'avg_shortest_path': 0 if g.number_of_edges()==0 else '%0.2f'%networkx.average_shortest_path_length(g),
            'avg_clustering': networkx.average_clustering(g),
            'distance': networkx.shortest_path_length(g, 0, ni),
            'degree': g.degree(ni),
        }
        
        # return json
        return JsonResponse(res)    
        
#HEATMAP FROM AUTHORS SUMMARY
columns_to_fetch = [
    'avg_nr_words',
    'avg_wordlen',
    'avg_words_gt6',
    'avg_personal',
    'avg_collective',
    'indegree',
    'indegree_centrality',
    'outdegree',
    'outdegree_centrality',
    'degree',
    'degree_centrality',
    'nr_posts',
    'hub_score',
    'authority_score',
    'betweeness_centrality',
    #'closeness_centrality',
    'polarity_arousal',
    'polarity_valence'        
]

class HeatmapView(CsrfExemptView):
    def post(self, request):
        input_json = json.loads(request.body)
        
        print input_json
        
        if input_json['parameters']['database'] not in connections:
            return jsonify(status='error', message="Invalid database!")
            
        if input_json['newsitems'] == '1' and input_json['comments'] == '1':
            author_ids_query = """
                SELECT DISTINCT author_id FROM comment
                UNION ALL
                SELECT DISTINCT author_id FROM author_newsitem
            """
        elif input_json['newsitems'] == '1':
            author_ids_query = "SELECT DISTINCT author_id FROM author_newsitem"
        elif input_json['comments'] == '1':
            author_ids_query = "SELECT DISTINCT author_id FROM comment"
        else:
            raise Exception("At least one of the options of newsitem or comment must be chosen")
            
        query = """
            SELECT {columns} 
            FROM ({author_ids_query}) AS comment_authors
            INNER JOIN author ON comment_authors.author_id = author.id
            INNER JOIN author_summary ON author.id = author_summary.author_id            
        """.format(columns = ",".join(columns_to_fetch),
                   author_ids_query = author_ids_query)
        
        cursor = connections[input_json['parameters']['database']].cursor()
        cursor.execute(query)
        
        message = ""
        results = []
        
        if cursor.rowcount == 0:
            message = "Query returned an empty result!"
        else:
            data_arrays = {}
            index = 0
            for column in columns_to_fetch:
                data_arrays[column] = {
                    'index': index,
                    'data': []   
                }
                results.append({'x': index, 'y': index, 'value': 1, 'correlation': 1})
                index += 1            
            
            for row in dictfetch(cursor):
                for column in columns_to_fetch:
                    data_arrays[column]['data'].append(row[column]) 
            
            combinatory_iterator = itertools.combinations(columns_to_fetch, 2)
            
            for col1, col2 in combinatory_iterator:
                col1_index = columns_to_fetch.index(col1)
                col2_index = columns_to_fetch.index(col2)
                coef = pearsonr(data_arrays[col1]['data'], 
                                data_arrays[col2]['data'])
                coef_0 = round(Decimal(coef[0]), 3)                              
                results.append({'x': col1_index, 'y': col2_index, 'value': coef_0, 'correlation': coef})
                results.append({'x': col2_index, 'y': col1_index, 'value': coef_0, 'correlation': coef})
            
        # make result
        res={
            'results': results,
            'columns': columns_to_fetch,
            'message': message                              
        }
        
        # return json
        return JsonResponse(res)    
        
class NewsitemsHeatmapView(CsrfExemptView):
    def post(self, request):
        input_json = json.loads(request.body)
        
        database = input_json['parameters']['database']
        
        if input_json['parameters']['database'] not in connections:
            return jsonify(status='error', message="Invalid database!")
        
        lotz_data_query = """
            SELECT newsitem.id nid, text.id tid, 
                                    text.wordcount,
                                    newsitem.qty_videos, 
                                    newsitem.qty_images, 
                                    LENGTH(text.text)/wordcount avg_wordlength,
                                    newsitem.qty_citations
              FROM newsitem, text
             WHERE newsitem.text_id = text.id        
        """
        
        qty_comments_query = """
            SELECT newsitem.id nid, COUNT(*) qty_comments
              FROM newsitem, comment
             WHERE comment.NewsItemID = newsitem.id
               AND newsitem.text_id IS NOT NULL
             GROUP BY nid        
        """
        
        comments_score_query = """
            SELECT newsitem_id nid, pos_comments, neg_comments, neutral_comments
              FROM newsitem, newsitem_pos_neg_comments 
             WHERE algorithm_id = %s
               AND newsitem.id = newsitem_id
               AND newsitem.text_id IS NOT NULL
        """                                          
        
        algorithm_results_query = """
            SELECT newsitem.id nid, result.value
            FROM newsitem, text, result
            WHERE newsitem.text_id = text.id
              AND text.id = result.text_id
              AND result.algorithm_id = %s      
        """
        
        algorithm_anew_valence, _ = Algorithm.objects.using(database)\
                                .get_or_create(name="anew_valence")
        algorithm_anew_arousal, _ = Algorithm.objects.using(database)\
                                            .get_or_create(name="anew_arousal")
        algorithm_anew_dominance, _ = Algorithm.objects.using(database)\
                                            .get_or_create(name="anew_dominance")        
                                    
        od_number_of_comments = OrderedDict()    
        
        cursor = connections[database].cursor()
        cursor.execute(lotz_data_query)                        
                                
        arr_number_of_words = []
        arr_number_of_images = []
        arr_number_of_videos = []
        arr_avg_wordlength = []
        arr_number_of_citations = []                        
                                
        for row in dictfetch(cursor):
            od_number_of_comments[row['nid']] = float(0)
            arr_number_of_words.append(float(row['wordcount']))
            arr_number_of_images.append(float(row['qty_images']))
            arr_number_of_videos.append(float(row['qty_videos']))
            arr_avg_wordlength.append(float(row['avg_wordlength']))
            arr_number_of_citations.append(float(row['qty_citations']))
            
        od_number_of_positive_comments = od_number_of_comments.copy()
        od_number_of_negative_comments = od_number_of_comments.copy()
        od_number_of_neutral_comments = od_number_of_comments.copy()
        od_valence = od_number_of_comments.copy()
        od_arousal = od_number_of_comments.copy()
        od_dominance = od_number_of_comments.copy()
        
        cursor.execute(comments_score_query, [input_json['algorithm']])
        for row in dictfetch(cursor):
            od_number_of_positive_comments[row['nid']] = float(row['pos_comments'])
            od_number_of_negative_comments[row['nid']] = float(row['neg_comments'])
            od_number_of_neutral_comments[row['nid']] = float(row['neutral_comments'])
        arr_number_of_positive_comments = od_number_of_positive_comments.values()
        arr_number_of_negative_comments = od_number_of_negative_comments.values()         
        arr_number_of_neutral_comments = od_number_of_neutral_comments.values()        
            
        cursor.execute(algorithm_results_query, [algorithm_anew_valence.id])
        for row in dictfetch(cursor):
            od_valence[row['nid']] = float(row['value'])     
        arr_valence = od_valence.values() 
            
        cursor.execute(algorithm_results_query, [algorithm_anew_arousal.id])
        for row in dictfetch(cursor):
            od_arousal[row['nid']] = float(row['value'])
        arr_arousal = od_arousal.values()
            
        cursor.execute(algorithm_results_query, [algorithm_anew_dominance.id])
        for row in dictfetch(cursor):
            od_dominance[row['nid']] = float(row['value'])
        arr_dominance = od_dominance.values()
                                 
        cursor.execute(qty_comments_query)
        for row in dictfetch(cursor):
            od_number_of_comments[row['nid']] = float(row['qty_comments'])
        arr_number_of_comments = od_number_of_comments.values()
        
        end = time.time()
            
        column_arrays = [
            arr_number_of_comments,
            arr_number_of_positive_comments,
            arr_number_of_negative_comments,
            arr_number_of_neutral_comments                
        ]
        row_arrays = [
            arr_number_of_words,
            arr_number_of_images,
            arr_number_of_videos,
            arr_avg_wordlength,
            arr_number_of_citations,
            arr_valence,
            arr_arousal,
            arr_dominance
        ]
        
        message = ""
        results = []
        
        for x_index in range(len(column_arrays)):    
            for y_index in range(len(row_arrays)):        
                
                if y_index >= 5:
                    coef = spearmanr(column_arrays[x_index], 
                                    row_arrays[y_index])
                    correlation = Decimal(coef[0])
                    value = round(correlation, 3)
                    probability = Decimal(float(coef[1].data))
                else:
                    coef = pearsonr(column_arrays[x_index], 
                                    row_arrays[y_index])
                    if numpy.isnan(coef[0]):
                        value = -1
                    else:
                        correlation = Decimal(coef[0])
                        value = round(correlation, 3)
                        probability = Decimal(coef[1])
                    
                results.append({'x': x_index, 
                                'y': y_index, 
                                'value': value, 
                                'correlation': (correlation, probability)})
            
        # make result
        res={
            'results': results,
            'message': message
        }
        
        # return json
        return JsonResponse(res)         
        
class MostInfluentialKeywordsView(CsrfExemptView):
    def post(self, request):
        input_json = json.loads(request.body)
        
        if input_json['parameters']['database'] not in connections:
            return jsonify(status='error', message="Invalid database!")     
            
        query = """
            SELECT keyword, count(*) amount FROM (
                SELECT text_id 
                  FROM comment
                 {date_where}
                 UNION ALL
                SELECT text_id
                  FROM newsitem
                 {date_where}
            ) AS news_comm_ids
            INNER JOIN text
               ON text.id = news_comm_ids.text_id
            INNER JOIN keyword
               ON keyword.text_id = text.id
            GROUP BY keyword
            ORDER BY amount DESC
            LIMIT 100
        """
        
        date_where = """
            WHERE DATE(date) >= '{date_min}'
              AND DATE(date) <= '{date_max}'
        """ 
        
        if input_json['date_min'] != "":
            formatted_date_where = date_where.format(
                date_min = input_json['date_min'],
                date_max = input_json['date_max'])
        else:
            formatted_date_where = ""
            
        formatted_query = query.format(date_where = formatted_date_where)         
        
        cursor = connections[input_json['parameters']['database']].cursor()
        cursor.execute(formatted_query)  
        
        results = []
        
        for row in dictfetch(cursor):        
            results.append({'text': row['keyword'], 'weight': row['amount']})
            
        return JsonResponse({'results': results})        
