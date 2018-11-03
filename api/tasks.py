from __future__ import absolute_import, unicode_literals

from bs4 import UnicodeDammit, BeautifulSoup
from collections import Counter, OrderedDict
import datetime
from decimal import Decimal
import itertools
import math
import time
import random
import requests

from gensim.models.word2vec import Word2Vec
import numpy
from scipy.stats import mannwhitneyu, wilcoxon, pearsonr
from sklearn.manifold import TSNE      

from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer

from pattern.en import lemma as lemmatizer_en
from pattern.nl import lemma as lemmatizer_nl

import word_processing.obo as obo
from word_processing.text_parser import TextProcessor   
                                
from django.db import connections

from celery import Task, shared_task
import numpy
from scipy.stats import mannwhitneyu as scipy_mannwhitneyu, wilcoxon, pearsonr

from rss_parser.models import Algorithm,\
                              Cat1,\
                              Category,\
                              Comment,\
                              Newsitem,\
                              Result     
                              
from api.common import StatisticFunctions
# Create your tasks here

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

class BaseTask(Task):
    abstract = True
    
    current_step = 0
    total_steps = 0
    #cs_ stands for current step ;)
    cs_name = "Starting..."
    cs_amount_done = 0
    cs_total_amount = 0
    
    _last_update = 0
    _last_amount = 0
    _last_amounts = []
    
    def __call__(self, *args, **kwargs):
        self.update_meta()
        return super(BaseTask, self).__call__(*args, **kwargs)
        
    def reset_amount(self):
        self.cs_amount_done = 0
        self._last_amount = 0
        self._last_update = 0
        self_last_amounts = []
    
    def increment_amount_done(self):
        self.cs_amount_done += 1
        self.calculate_status_update()
    
    def update_amount_done(self, amount):
        self.cs_amount_done = amount
        self.calculate_status_update()
            
    def update_meta(self, perc_done=0, eta=""):
        self.update_state(state="PROGRESS", meta={
            'current_step': self.current_step,
            'total_steps': self.total_steps,
            'cs_name': self.cs_name,
            'cs_amount_done': self.cs_amount_done,
            'cs_total_amount': self.cs_total_amount,
            'cs_perc_done': perc_done,
            'eta': eta
        })
        
    def calculate_status_update(self, force=False):
        if time.time() - self._last_update > 10 or force:
            perc_done = (float(self.cs_amount_done)/self.cs_total_amount)*100
            if len(self._last_amounts) > 1:
                avg_mileage_per_s = numpy.average(self._last_amounts) / 10
                remaining_seconds = (self.cs_total_amount - self.cs_amount_done) / avg_mileage_per_s
                m, s = divmod(remaining_seconds, 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)
                eta = ""
                if d > 0:
                    eta += "{}d ".format(int(d))
                if h > 0:
                    eta += "{}h ".format(int(h))
                if m > 0:
                    eta += "{}m ".format(int(m))
                if s > 0:
                    eta += "{}s ".format(int(s))                    
            else:
                eta = "calculating..."
            self.update_meta(perc_done, eta)
            if self.cs_amount_done > 0:
                self._last_amounts.append(self.cs_amount_done - self._last_amount)
            self._last_amount = self.cs_amount_done
            if len(self._last_amounts) > 10:
                del self._last_amounts[0]
            self._last_update = time.time()
            
    

@shared_task(bind=True, base=BaseTask)
def waiter(self, iterations, force_error=False):
    iterations = int(iterations)
    self.cs_total_amount = iterations
    for i in range(iterations):
        self.update_amount_done(i)
        time.sleep(1)
    if force_error:
        raise Exception("Forced error!")
    return "Succesful!"
    
class StatisticTask(BaseTask, StatisticFunctions):
    pass

@shared_task(bind=True, base=StatisticTask)
def mannwhitneyu(self, database, algorithm, start_month, end_month): 
    self.total_steps = 3
    
    self.set_start_end_months(start_month, end_month)
    
    algorithm = Algorithm.objects.using(database)\
                                 .get(id=int(algorithm))
    
    query = """
        SELECT newsitem.cat1, result.value
          FROM newsitem, text, result
         WHERE newsitem.text_id = text.id
           AND text.id = result.text_id 
           AND result.algorithm_id = %s 
           AND newsitem.date >= %s
           AND newsitem.date <= %s
    """
    
    cursor = connections[database].cursor()
    cursor.execute(query, [algorithm.id, self.start_date, self.end_date])
    
    self.cs_name = "Getting data"
    self.current_step = 1
    self.cs_total_amount = cursor.rowcount
    self.reset_amount()
    self.update_meta()
    
    newsitems_by_cat = {}
    while True:
        row = cursor.fetchone()
        if row == None:
            break
        cat1, value = row
        if cat1 is None:
            pass
        elif not cat1 in newsitems_by_cat:
            newsitems_by_cat[cat1] = [Decimal(value)]
        else:
            newsitems_by_cat[cat1].append(Decimal(value))
        self.increment_amount_done()
        
    self.current_step = 2
    self.cs_name = "Organizing Data"
    self.reset_amount()
    self.cs_total_amount = 0    
    self.update_meta()
            
    cat_keys = newsitems_by_cat.keys()
    cat_keys.sort()
    
    categories = Cat1.objects\
                .using(database)\
                .filter(id__in=cat_keys)
    cat_labels = [cat.label for cat in categories]

    category_data = []             
    results = []
    
    self.current_step = 3
    self.cs_name = "Processing data"
    self.reset_amount()
    self.cs_total_amount = len(cat_keys) ^ 2
    self.update_meta()
    
    print cat_keys
    print cat_labels
    
    for cat1, cat_label in itertools.izip(cat_keys, cat_labels):
        cat_results = []
        for cat2 in cat_keys:
            try:
                value = scipy_mannwhitneyu(x=newsitems_by_cat[cat1], 
                                           y=newsitems_by_cat[cat2])
            except Exception as e:
                result = ("N/A","N/A")
            if value == '0':
                cat_results.append({
                    'testing_value': 0,
                    'significance': 0
                })
            else:       
                cat_results.append({
                    'testing_value': value[0],
                    'significance': value[1]
                })
            self.increment_amount_done()
        results.append({
            'name': cat_label,
            'results': cat_results,
            'amount_of_data': len(newsitems_by_cat[cat1])
        })
    
    return {'results': results}            
    
@shared_task(bind=True, base=StatisticTask)
def wilcoxonmonthly(self, database, category, algorithm, start_month, end_month):    
    self.total_steps = 2
    self.set_start_end_months(start_month, end_month)
    
    category = Cat1.objects.using(database)\
                           .get(id=int(category))
                           
    algorithm = Algorithm.objects.using(database)\
                                 .get(id=int(algorithm))
    
    query = """
        SELECT newsitem.date, result.value 
          FROM newsitem, text, result, algorithm
         WHERE newsitem.text_id = text.id            
           AND result.text_id = text.id
           AND result.algorithm_id = algorithm.id      
           AND algorithm.name = %s
           AND newsitem.cat1 = %s      
           AND newsitem.date >= %s
           AND newsitem.date <= %s               
    """
    
    cursor = connections[database].cursor()
    cursor.execute(query, [algorithm.name, 
                           category.id, 
                           self.start_date,
                           self.end_date])
    months = []
                
    newsitems_by_month = {}
    
    self.cs_name = "Getting data"
    self.cs_total_amount = cursor.rowcount
    
    for row in cursor.fetchall():
        month_year_key = "{}/{}".format(row[0].month, 
                                        row[0].year)
        if not month_year_key in newsitems_by_month:
            newsitems_by_month[month_year_key] = [Decimal(row[1])]
        else:
            newsitems_by_month[month_year_key].append(Decimal(row[1]))
        self.increment_amount_done()
            
    headers = []        
    results = []
    
    self.current_step = 2
    self.cs_name = "Processing data"
    self.cs_amount_done = 0
    self.cs_total_amount = len(newsitems_by_month)    
    self.update_meta()
    
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
                    if numpy.isnan(result[0]) or numpy.isnan(result[1]):
                        result = ("N/A","N/A")
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
        self.increment_amount_done()
    
    return {'headers': headers,
            'results': results}      
            
@shared_task(bind=True, base=StatisticTask)
def wilcoxoninterval(self, database, 
                           category, 
                           algorithm, 
                           start_date1, 
                           start_date2, 
                           end_date1, 
                           end_date2):     
    
    mask = '%Y-%M-%d'
    
    start_date1 = datetime.datetime.strptime(start_date1, mask)
    start_date2 = datetime.datetime.strptime(start_date2, mask)
    end_date1 =   datetime.datetime.strptime(end_date1  , mask)
    end_date2 =   datetime.datetime.strptime(end_date2  , mask)
    
    self.current_step = 1
    self.total_steps = 2
    self.reset_amount()
    self.cs_total_amount = 4    
    self.cs_name = "Getting data"
    self.update_meta()
    
    category = Cat1.objects.using(database)\
                           .get(id=int(category))
    self.increment_amount_done()
    algorithm = Algorithm.objects.using(database)\
                                 .get(id=int(algorithm))
    self.increment_amount_done()
    
    query = """
        SELECT result.value 
          FROM newsitem, text, result, algorithm
         WHERE newsitem.text_id = text.id
           AND result.text_id = text.id
           AND result.algorithm_id = algorithm.id
           AND algorithm.name = %s
           AND newsitem.cat1 = %s     
           AND newsitem.date >= %s
           AND newsitem.date <= %s               
    """
    
    cursor = connections[database].cursor()      
    
    #Running query for interval 1
    cursor.execute(query, [algorithm.name, 
                           category.id, 
                           start_date1,
                           end_date1])
    results1 = [Decimal(row[0]) for row in cursor.fetchall()]     
    self.increment_amount_done()
    
    #Running query for interval 2
    cursor.execute(query, [algorithm.name, 
                           category.id, 
                           start_date2,
                           end_date2])
    results2 = [Decimal(row[0]) for row in cursor.fetchall()]     
    self.increment_amount_done()
    
    self.current_step = 2
    self.reset_amount()
    self.cs_total_amount = 0 
    self.cs_name = "Calculating"
    self.update_meta()    
    
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
    
    return {'results': {'testing_value': result[0],
                        'significance': result[1]}}    
                        
     
text_processor = TextProcessor()    

re_vowel_en = re.compile("[aAeEiIoOuU]")
re_vowel_nl = re.compile("IJ|ij|[aAeEiIoOuU]")     
     
@shared_task(bind=True, base=StatisticTask)
def wordprocessing(self, database, 
                         language,   
                         lemmatizer, 
                         news_comments, 
                         news_comments_start_date, 
                         news_comments_end_date, 
                         exclude_vowels,
                         stopwords,                 
                         stemmer,
                         upload_textarea,
                         upload_option,
                         ignore_results_amount,
                         upload_url):     

    self.total_steps = 7

    self.current_step = 1
    self.cs_name = "Initializing"
    self.reset_amount()
    self.cs_total_amount = 0    
    self.update_meta()
    
    #Language check
    if language not in ['english', 'dutch']:
        return {'status':'error', 'message':"Invalid language!"}
        
    if database not in connections:
        return {'status':'error', 'message':"Invalid database!"}
        
    self.current_step = 2
    self.cs_name = "Normalizing Input"   
    self.reset_amount()
    self.cs_total_amount = 0    
    self.update_meta()        
    
    #Input normalization
    if upload_option == 'text_field':
        input_text = upload_textarea
    elif upload_option == 'url':
        page_text = requests.get(upload_url).text
        soup = BeautifulSoup(page_text, "html.parser")
        input_text = soup.text
    elif upload_option == 'file':
        input_text = UnicodeDammit(upload_file.read()).unicode_markup
    elif upload_option == 'news_comments':
        start_date_text = news_comments_start_date
        end_date_text = news_comments_end_date
        start_date = datetime.date(*[int(i) for i in start_date_text.split('-')])
        end_date = datetime.date(*[int(i) for i in end_date_text.split('-')])
        filters = {
            'date__gte': start_date,   
            'date__lte': end_date,
            'text__isnull': False
        }
        input_text = ""
        if news_comments in ['news', 'news_comments']:
            self.cs_name = "Normalizing Input - Reading Newsitems"
            queryset = Newsitem.objects\
                               .using(database)\
                               .filter(**filters)\
                               .select_related('text')
            self.cs_total_amount = queryset.count()                               
            for newsitem in queryset:
                input_text += "\n"+newsitem.text.text
                self.increment_amount_done()
        if news_comments in ['comments', 'news_comments']:
            self.cs_name = "Normalizing Input - Reading Comments"
            queryset = Comment.objects\
                       .using(database)\
                       .filter(**filters)\
                       .select_related('text')
            self.cs_total_amount = queryset.count() 
            for comment in queryset:    
                input_text += "\n"+comment.text.text   
                self.increment_amount_done()
                
    #Stemmer selection
    if stemmer == 'no_stemmer':
        stemmer = None
    elif stemmer == 'porter':
        if language != 'english':
            return jsonify(status='error', message="Invalid language for stemmer porter!")
        stemmer = PorterStemmer()
    elif stemmer == 'snowball':
        stemmer = SnowballStemmer(language)
    else:
        return jsonify(status='error', message="Invalid stemmer!")
            
    #Lemmatizer selection
    if lemmatizer == 'lemmatizer_off':
        lemmatizer = None
    elif language == 'english':
        lemmatizer = lemmatizer_en
    else:
        lemmatizer = lemmatizer_nl
        
    #Stopwords selection    
    if stopwords == 'no_stopwords':    
        stopwords = None
    elif stopwords == 'our_stopwords':
        stopwords = obo.stopwords
    elif stopwords == 'custom_stopwords':
        custom_stopword_text = UnicodeDammit(input_json.get('custom_stopword_file').read()).unicode_markup
        stopwords = obo.stripNonAlphaNum(custom_stopword_text)
        
    self.current_step = 3
    self.cs_name = "Wordlist creation"
    self.reset_amount()
    self.cs_total_amount = len(input_text)    
    self.update_meta()         
        
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
                if exclude_vowels == 'exclude_vowels_yes':
                    if language == 'english':
                        regex = re_vowel_en
                    else:
                        regex = re_vowel_nl
                    processed_word = regex.sub("", processed_word)
                resulting_text += processed_word
                final_wordlist.append(processed_word)
        self.cs_amount_done += len(word)
        self.calculate_status_update()
    
    self.current_step = 4
    self.cs_name = "obo.wordListToFreqDict"
    self.reset_amount()
    self.cs_total_amount = 0    
    self.update_meta() 
    
    dictionary = obo.wordListToFreqDict(final_wordlist)
    
    self.current_step = 5
    self.cs_name = "obo.sortFreqDict"
    self.reset_amount()
    self.cs_total_amount = 0    
    self.update_meta()     
    
    sorteddict = obo.sortFreqDict(dictionary)   
    
    self.current_step = 6
    self.cs_name = "Dealing with Ignored Results"
    self.reset_amount()
    self.cs_total_amount = 0
    self.update_meta()   
    
    ignore_results_amount = int(ignore_results_amount)  
      
    if ignore_results_amount > 0:
        self.cs_total_amount = len(resulting_text)
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
            self.cs_amount_done += len(word)
            self.calculate_status_update()                
        resulting_text = new_text
        final_wordlist = new_wordlist
    else:
        initial_index = 0          
    
    self.current_step = 7
    self.cs_name = "Doing the math"
    self.reset_amount()
    self.cs_total_amount = 0    
    self.update_meta()   
    
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
        
    return {'results': {'status': 'success', 
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
                        'sorteddict': sorteddict}}