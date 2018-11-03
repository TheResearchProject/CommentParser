# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-18 07:44
from __future__ import unicode_literals

from nltk.tokenize import RegexpTokenizer

from django.db import migrations, models, transaction

from rss_parser.models import Comment, Newsitem, Text

from comment_parser.queryset_iterator import queryset_iterator

from progressbar import ProgressBar, \
    SimpleProgress, Percentage, Bar, Timer, AdaptiveETA

@transaction.atomic
def forward(apps, schema_editor):
    migrate(apps, schema_editor, 'forward')
            
@transaction.atomic            
def backwards(apps, schema_editor):
    migrate(apps, schema_editor, 'backwards')
            
def migrate(apps, schema_editor, direction):
    pbar_widgets = [SimpleProgress(),
       ' ', Percentage(),
       ' ', Bar(),
       ' ', Timer(),
       ' ', AdaptiveETA()]     
    
    for model in ['Comment', 'Newsitem']:
        queryset = globals()[model].objects.filter(text__isnull=True)
        if queryset.count() == 0:
            continue
        print "Processing " + model
        pbar = ProgressBar(widgets=pbar_widgets, maxval=queryset.count())
        done = 0
        pbar.start()               
        tokenizer = RegexpTokenizer(r'\w+')
        for item in queryset_iterator(queryset, chunksize=20):
            if item.content:
                if direction == "forward":
                    item.text = Text.objects.create(
                        text=item.content,
                        wordcount=len(tokenizer.tokenize(item.content)))
                elif direction == "backwards":
                    item.content = item.text.text
                item.save()
                done += 1
                pbar.update(done)       
        pbar.finish()

class Migration(migrations.Migration):

    dependencies = [
        ('rss_parser', '0018_auto_20160729_1243'),
    ]

    operations = [
        migrations.RunPython(forward, backwards),
    ]
