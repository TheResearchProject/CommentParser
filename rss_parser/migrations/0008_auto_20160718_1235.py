# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-18 12:35
from __future__ import unicode_literals

from django.db import migrations, transaction

from rss_parser.models import Comment, Text, Word

@transaction.atomic
def forward(apps, schema_editor):
    words = Word.objects.all()
    for word in words:
        word.text = word.comment.text
        word.save()
            
@transaction.atomic            
def backwards(apps, schema_editor):
    words = Word.objects.all()
    for word in words:
        word.comment.text = word.text 
        word.save()

class Migration(migrations.Migration):

    dependencies = [
        ('rss_parser', '0007_word_text'),
    ]

    operations = [
        migrations.RunPython(forward, backwards),
    ]
