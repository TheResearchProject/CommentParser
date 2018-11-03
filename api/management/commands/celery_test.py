import pdb

from django.core.management.base import BaseCommand, CommandError

from api.tasks import add

class Command(BaseCommand):
    help = 'Testing Celery'

    def handle(self, *args, **options):
        res = add.delay(2,3)
        
        pdb.set_trace()
        pass

        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))