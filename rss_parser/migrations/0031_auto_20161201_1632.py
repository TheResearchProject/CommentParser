# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-01 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss_parser', '0030_auto_20161201_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorsummary',
            name='authority_score',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='avg_collective',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='avg_nr_words',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='avg_personal',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='avg_shared',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='avg_wordlen',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='avg_words_gt6',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='betweeness_centrality',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='closeness_centrality',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='clustering_coef',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='constraint',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='degree',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='degree_centrality',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='eccentricity',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='hub_score',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='indegree',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='indegree_centrality',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='nr_posts',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='outdegree',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='outdegree_centrality',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='pagerank',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='pagerank_weighted',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='polarity_arousal',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='authorsummary',
            name='polarity_valence',
            field=models.FloatField(blank=True),
        ),
    ]
