# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 12:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss_parser', '0013_algorithm_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]