# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-20 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_gensim', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='word',
            name='dictionary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='django_gensim.Dictionary'),
        ),
    ]