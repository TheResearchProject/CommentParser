import pdb
import pprint

from celery.result import AsyncResult
from comment_parser.celery import app   

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Kills a Celery Task'

    def add_arguments(self, parser):
        parser.add_argument('task-id')

    def handle(self, *args, **options):
        
        res = AsyncResult(options['task-id'], app=app)
        pdb.set_trace()
        res.revoke(terminate=True, signal="SIGKILL")
        self.stdout.write(self.style.SUCCESS(
            'Successfully killed task "%s"' % res.id))
            