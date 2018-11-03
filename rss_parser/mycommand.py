import pdb
from argparse import ArgumentTypeError as err
import os

from django.core.management.base import BaseCommand
from django.db import connections

from comment_parser.progressbarwrapper import ProgressBarWrapper
    
from .models import Comment, Newsitem, Text    

class PathType(object):
    def __init__(self, exists=True, type='file', dash_ok=True):
        '''exists:
                True: a path that does exist
                False: a path that does not exist, in a valid parent directory
                None: don't care
           type: file, dir, symlink, None, or a function returning True for valid paths
                None: don't care
           dash_ok: whether to allow "-" as stdin/stdout'''

        assert exists in (True, False, None)
        assert type in ('file','dir','symlink',None) or hasattr(type,'__call__')

        self._exists = exists
        self._type = type
        self._dash_ok = dash_ok

    def __call__(self, string):
        if string=='-':
            # the special argument "-" means sys.std{in,out}
            if self._type == 'dir':
                raise err('standard input/output (-) not allowed as directory path')
            elif self._type == 'symlink':
                raise err('standard input/output (-) not allowed as symlink path')
            elif not self._dash_ok:
                raise err('standard input/output (-) not allowed')
        else:
            e = os.path.exists(string)
            if self._exists==True:
                if not e:
                    raise err("path does not exist: '%s'" % string)

                if self._type is None:
                    pass
                
        return string

class MyCommand(BaseCommand):
    #Sets the available type of item to be used in processing (newsitems, comments or '*' for both)
    items_used = "*"
    db_names = []
    selected_dbs = []
    
    def add_arguments(self, parser):
        parser.add_argument('--alternate-pbar', action='store_true', 
                                                default=False,
                                                help="Show progress in a way more suitable for log files.")
        
        db_group = parser.add_argument_group(title='Sources', description="Available databases to source from. You can select more than one database. If none is selected, will use all of them.")
        for database in connections.databases:
            if database != 'default':
                self.db_names.append(database)
                db_group.add_argument('--db-'+database, action='store_true',
                                                        help="Use database " + database)

        if self.items_used == "*":
            item_group = parser.add_argument_group(title='Items', description="Items to use in the process. If none selected, all of them will be used.")
            item_group.add_argument('--only-newsitems', action='store_true',
                                                        help="Process only Newsitems.")
            item_group.add_argument('--only-comments', action='store_true',
                                                       help="Process only Comments.")
        else:
            item_group = parser.add_argument_group(title='Items', description="Items to use in the process. This command used only {}.".format(self.items_used))
        
        
    def handle(self, *args, **options):    
        self.alternate_pbar = options['alternate_pbar']
        for database in self.db_names:
            if options['db_'+database]:
                self.selected_dbs.append(database)
        if len(self.selected_dbs) == 0:
            self.selected_dbs = self.db_names
        
    #seems silly, but I'm keeping these methods for backwards compatibility    
    def pbar_setup(self, maxval):
        self.pbar = ProgressBarWrapper(maxval, self.alternate_pbar)       
        
    def pbar_increment(self):
        self.pbar.increment()  
        
    def pbar_destroy(self):
        self.pbar.destroy()
        
