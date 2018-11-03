"""comment_parser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^create-task/', create_task),
    url(r'^get-task-status/', get_task_status),
    url(r'^kill-task/', kill_task),
    url(r'^available_models/', available_models),
    url(r'^calculate_vectors/', calculate_vectors),
    url(r'^mannwhitneyu/', MannWhitneyUView.as_view()),
    url(r'^wilcoxonmonthly/', WilcoxonMonthlyView.as_view()),
    url(r'^wilcoxoninterval/', WilcoxonIntervalView.as_view()),
    url(r'^word-processing/', WordProcessingView.as_view()),
    url(r'^netvis-data/', NetvisDataView.as_view()),
    url(r'^netvis-graph-info/', NetvisGraphInfoView.as_view()),
    url(r'^heatmap/', HeatmapView.as_view()),
    url(r'^newsitems-heatmap/', NewsitemsHeatmapView.as_view()),
    url(r'^most-influential-keywords/', MostInfluentialKeywordsView.as_view()),
]
