import cPickle
import datetime
from decimal import Decimal
import itertools
import pdb
import pprint
import random
import re

import numpy
from scipy.stats import mannwhitneyu, wilcoxon

from django.conf import settings
from django.db import connections
from django.shortcuts import render
from django.views.generic import View

from rss_parser.models import Algorithm, Cat1, Newsitem, Result

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
    
class StatisticView(View):
    def get_months(self):
        cursor = connections[self.database].cursor()  
        sql = "SELECT DISTINCT MONTH(Date), YEAR(Date) FROM `newsitem` ORDER BY YEAR(Date), MONTH(Date) ASC"
        cursor.execute(sql)
        months = []
        for row in cursor.fetchall():
            months.append("{}/{}".format(row[0], row[1]))
        return months
        
    def get_context(self):
        return {
            'selected_database':self.database,
            'databases':settings.AVAILABLE_DATABASES,
            'algorithms': Algorithm.objects.using(self.database).all()
        }

    def set_database(self, request_dict):
        if 'database' in request_dict and request_dict['database'] in settings.AVAILABLE_DATABASES:
            self.database = request_dict['database']
        else:
            self.database = settings.AVAILABLE_DATABASES[0]
        

    def get(self, request):
        self.set_database(request.GET)
            
    def post(self, request):
        self.set_database(request.POST)
        
        month_regex = re.compile('(\d+)/(\d+)')
        
        start_month, start_year = month_regex.match(request.POST['start_month']).groups()
        start_month = int(start_month)
        start_year = int(start_year)
        self.start_date = datetime.date(start_year, start_month, day=1)
        
        end_month, end_year = month_regex.match(request.POST['end_month']).groups()
        end_month = int(end_month)
        end_year = int(end_year)
        self.end_date = datetime.date(end_year, end_month, day=1) + datetime.timedelta(days=30)
        while self.end_date.month > end_month:
            self.end_date -= datetime.timedelta(days=1)
                

class MannWhitneyUView(StatisticView):
    
    def get_context(self):
        context = super(MannWhitneyUView, self).get_context()    
        context['months'] = self.get_months()
        return context
        
    def get(self, request):
        super(MannWhitneyUView, self).get(request)
        return render(request, 'statistics/mannwhitneyu.html', self.get_context())
        
    def post(self, request):
        super(MannWhitneyUView, self).post(request)
        
        context = self.get_context()
        
        context['start_month'] = request.POST['start_month']
        context['end_month'] = request.POST['end_month']
        
        algorithm = Algorithm.objects.using(self.database)\
                                     .get(id=request.POST['algorithm'])
        context['selected_algorithm'] = algorithm
        
        query = """
            SELECT newsitem.cat1, result.value 
              FROM newsitem, text, result, algorithm
             WHERE newsitem.text_id = text.id
               AND result.text_id = text.id
               AND result.algorithm_id = algorithm.id
               AND newsitem.cat1 is not null
               AND algorithm.name = %s
               AND newsitem.date >= %s
               AND newsitem.date <= %s
        """
        
        cursor = connections[self.database].cursor()
        cursor.execute(query, [algorithm.name, self.start_date, self.end_date])
        
        newsitems_by_cat = {}
        for row in cursor.fetchall():
            cat1, value = row
            if not cat1 in newsitems_by_cat:
                newsitems_by_cat[cat1] = [Decimal(value)]
            else:
                newsitems_by_cat[cat1].append(Decimal(value))
                
        cat_keys = newsitems_by_cat.keys()
        cat_keys.sort()
        
        pprint.pprint(cat_keys)

        categories = Cat1.objects\
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
        
        context['results'] = results
        context['category_data'] = category_data
        
        return render(request, 'statistics/mannwhitneyu.html', context)
        
class WilcoxonMonthlyView(StatisticView):

    def get_context(self):
        context = super(WilcoxonMonthlyView, self).get_context()
        categories = Cat1.objects\
                         .using(self.database)\
                         .all()
        context['categories'] = [cat.label for cat in categories]
        context['months'] = self.get_months()
        return context
        
    def get(self, request):
        super(WilcoxonMonthlyView, self).get(request)
        return render(request, 'statistics/wilcoxon.html', self.get_context())      
        
    def post(self, request):
        super(WilcoxonMonthlyView, self).post(request)
        
        context = self.get_context()
        
        context['start_month'] = request.POST['start_month']
        context['end_month'] = request.POST['end_month']
        
        category = Cat1.objects.using(self.database)\
                               .get(label=request.POST['category'])
                               
        context['category'] = category
        
        algorithm = Algorithm.objects.using(self.database)\
                                     .get(id=request.POST['algorithm'])
        context['selected_algorithm'] = algorithm
        
        query = """
            SELECT newsitem.date, result.value 
              FROM newsitem, text, result, algorithm
             WHERE newsitem.text_id = text.id
               AND result.text_id = text.id
               AND result.algorithm_id = algorithm.id
               AND algorithm.name = %s
               AND cat1 = %s
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
        
        return render(request, 'statistics/wilcoxon.html', context)        
        
class WilcoxonIntervalView(StatisticView):

    def get_context(self):
        context = super(WilcoxonIntervalView, self).get_context()
        categories = Cat1.objects\
                         .using(self.database)\
                         .all()
        context['categories'] = [cat.label for cat in categories]
        return context
        
    def get(self, request):
        super(WilcoxonIntervalView, self).get(request)
        return render(request, 'statistics/wilcoxon_interval.html', self.get_context())      
        
    def post(self, request):
        self.set_database(request.POST)
        
        context = self.get_context()
        
        pprint.pprint(request.POST)

        mask = '%d-%b-%Y'
        
        context['start_date1'] = datetime.datetime.strptime(request.POST['start_date1'], mask)
        context['start_date2'] = datetime.datetime.strptime(request.POST['start_date2'], mask)
        context['end_date1'] =   datetime.datetime.strptime(request.POST['end_date1']  , mask)
        context['end_date2'] =   datetime.datetime.strptime(request.POST['end_date2']  , mask)
        
        category = Cat1.objects.using(self.database)\
                               .get(label=request.POST['category'])
                               
        context['category'] = category
        
        algorithm = Algorithm.objects.using(self.database)\
                                     .get(id=request.POST['algorithm'])
        context['selected_algorithm'] = algorithm
        
        query = """
            SELECT result.value 
              FROM newsitem, text, result, algorithm
             WHERE newsitem.text_id = text.id
               AND result.text_id = text.id
               AND result.algorithm_id = algorithm.id
               AND algorithm.name = %s
               AND cat1 = %s
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
        
        context['result'] = {
            'testing_value': result[0],
            'significance': result[1]               
        }
        
        return render(request, 'statistics/wilcoxon_interval.html', context)        
        