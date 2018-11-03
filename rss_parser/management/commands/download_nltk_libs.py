from django.core.management.base import BaseCommand, CommandError

import nltk

class Command(BaseCommand):
    help = 'Downloads the needed libraries from NLTK'
    
    def handle(self, *args, **options):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')
