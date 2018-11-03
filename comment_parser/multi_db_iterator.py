import itertools
import pdb

from django.db import connections

from comment_parser.queryset_iterator import queryset_iterator

class MultiDbIterator():
    def __init__(self, model, databases=None, chunksize = 50):
        self.model = model
        self.chunksize = chunksize
        self.total_count = 0
        self.querysets = []
        if databases:
            self.databases = databases
        else:
            self.databases = []
            for database in connections.databases:
                if database != 'default':    
                    self.databases.append(database)
                    
    def query(self, filters=None, only=None):
        for database in self.databases:
            queryset = self.model.objects.using(database)
            if filters:
                queryset = queryset.filter(**filters)
            if only:
                queryset = queryset.only(*only)
            self.querysets.append(queryset)
            self.total_count += queryset.count()    

    def get_iterator(self):
        return itertools.chain.from_iterable(
            [queryset_iterator(queryset, chunksize=self.chunksize) for queryset in self.querysets])
