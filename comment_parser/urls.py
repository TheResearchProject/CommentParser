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
from django.conf.urls import include, url
from django.contrib import admin

from django_js_reverse.views import urls_js as js_reverse_urls_js

from .views import available_databases, index

urlpatterns = [
    url(r'^$', index),
    url(r'^admin/', admin.site.urls),
    url(r'^available_databases/$', available_databases),
    url(r'^jsreverse/$', js_reverse_urls_js, name='js_reverse'),
    url(r'^lda_stats/', include('lda_stats.urls')),
    url(r'^netvis/', include('netvis.urls')),
    url(r'^statistics/', include('statistics.urls')),
    url(r'^word_processing/', include('word_processing.urls')),
    url(r'^api/', include('api.urls')),
]
