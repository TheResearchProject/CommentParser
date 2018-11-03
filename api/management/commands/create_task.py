import argparse
import pdb
import pprint

from django.core.management.base import BaseCommand, CommandError

import api.tasks 

class Command(BaseCommand):
    help = 'Create a Celery task'
    
    def add_arguments(self, parser):
        parser.add_argument('task-name')
        parser.add_argument('arguments', nargs=argparse.REMAINDER)

    def handle(self, *args, **options):
        
        pprint.pprint(options)
        
        task_ok = False
        try:
            res = getattr(api.tasks, options['task-name']).delay(*options['arguments'])
            task_ok = True
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                'Error while creating task: {}'.format(e.message)))
        if not task_ok:
            return
            
        self.stdout.write(self.style.SUCCESS(
            'Successfully created task "%s"' % res.id))