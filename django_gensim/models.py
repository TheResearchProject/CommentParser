from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Dictionary(models.Model):
    pass

class Word(models.Model):
    dictionary = models.ForeignKey('Dictionary', null=True)
    sequence = frequency = models.IntegerField(null=True) 
    word = models.CharField(max_length=255)
    frequency = models.IntegerField(default=0)
    amount_of_documents = models.IntegerField(default=1)
    