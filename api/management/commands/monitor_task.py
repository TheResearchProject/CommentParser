import pdb
import pprint
import time

from celery.result import AsyncResult
from comment_parser.celery import app   

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Testing Celery'

    def add_arguments(self, parser):
        parser.add_argument('task-id')

    def handle(self, *args, **options):
        
        res = AsyncResult(options['task-id'], app=app)
        
        while True:
            pprint.pprint({
                'state': res.state,
                'info': res.info
            })
            time.sleep(10)
            if res.state == 'SUCCESS':
                break
        
        self.stdout.write(self.style.SUCCESS("Finished"))
            