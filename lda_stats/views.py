import json

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from rss_parser.models import ExtraSettings, GeneralStats, HotTopics, Newsitem

# Create your views here.

def general_stats(request):
    stats = GeneralStats.objects.all()
    stats_dic = {}
    for stat in stats:
        stats_dic[stat.stat_name] = stat.stat_value
    return HttpResponse(json.dumps(stats_dic))
    
def hot_topics(request):
    algorithm = request.GET["algorithm"] if "algorithm" in request.GET else "lda"
    period = request.GET["period"] if "period" in request.GET else 1

    result = HotTopics.objects.filter(algorithm = algorithm, period = period)
    
    topics = [r.topics for r in result]
    return HttpResponse(json.dumps(topics))
    
def influential_items(request):
    result = Newsitem.objects.annotate(num_comments=Count('comment'))\
                             .order_by('-num_comments')[:25]    
    items = [{"title": r.title, "count": r.num_comments} for r in result]
    return HttpResponse(json.dumps(items))
    
def influential_words(request):
    setting = ExtraSettings.objects.filter(setting_name='influential_tfidf').first()
    return HttpResponse(setting.setting_value)    