import pdb
import pprint

from celery.result import AsyncResult
from comment_parser.celery import app   

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Testing Celery'

    def add_arguments(self, parser):
        parser.add_argument('task-id')

    def handle(self, *args, **options):
        
        res = AsyncResult(options['task-id'], app=app)
        
        if res.state == "PENDING":
            self.stdout.write(self.style.ERROR(
                'ERROR: task with id {} state is "PENDING"'.format(options['task-id'])))
            return
        
        self.stdout.write("=== The result is: ===")
        pprint.pprint(res.get())
        self.stdout.write("=== End of results ===")
            