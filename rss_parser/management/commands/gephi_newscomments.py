import argparse
import codecs
import datetime
import pdb
from xml.etree.ElementTree import Element,\
                                  ElementTree,\
                                  SubElement,\
                                  Comment,\
                                  tostring

from rss_parser.mycommand import MyCommand

from rss_parser.models import Comment, Newsitem

from comment_parser.queryset_iterator import queryset_iterator

class Command(MyCommand):
    help = 'Calculate the hot topics'
    items_used = "*"
    
    def add_arguments(self, parser):
        parser.add_argument('output', type=argparse.FileType('w'))
        super(Command, self).add_arguments(parser)    
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        if len(self.selected_dbs) != 1:
            self.stdout.write(self.style.ERROR('You need to select exactly one database for this command'))
            return
            
        selected_db = self.selected_dbs[0]
            
        nodes = Element('nodes')
        edges = Element('edges')
        
        self.stdout.write("Processing NewsItems")
        
        queryset = Newsitem.objects.using(selected_db).only('id').all()
        self.pbar_setup(maxval=queryset.count())
        
        for newsitem in queryset_iterator(queryset, chunksize=10000):
            nodes.append(Element('node', attrib={
                'id': "N{}".format(newsitem.id),
                'label': "Newsitem {}".format(newsitem.id),
            }))
            
            self.pbar_increment()
    
        self.pbar_destroy()       
        
        self.stdout.write("Processing Comments")
        
        queryset = Comment.objects.using(selected_db)\
                                  .only('id', 'parent_id', 'newsitem_id')\
                                  .all()
        edge_id = 0
        self.pbar_setup(maxval=queryset.count())
        
        for comment in queryset_iterator(queryset, chunksize=10000):
            comment_id = "C{}".format(comment.id) 
            nodes.append(Element('node', attrib={
                'id': comment_id,
                'label': "Comment {}".format(comment.id),
            }))
            
            if comment.parent_id:
                target_id = comment_id
            else:
                target_id = "N{}".format(comment.newsitem_id)
                
            edges.append(Element('edge', attrib={
                'id': str(edge_id),
                'source': comment_id,
                'target': target_id,
                'type': 'directed'
            }))
            
            edge_id += 1
            
            self.pbar_increment()
    
        self.pbar_destroy()       
        
        self.stdout.write("Finishing...")
            
        graph = Element('graph', attrib={
            'mode': 'dynamic',
            'defaultedgetype': 'directed',
        })
        
        graph.append(nodes)
        graph.append(edges)
        
        meta = Element('meta', attrib={
            'lastmodifieddate': datetime.date.today().isoformat()
        })
        
        meta.append(Element('creator', text="Iris Steenhout"))
        meta.append(Element('description', text="Newsitems and it's comments."))
        
        gexf = Element('gexf', attrib={
            'xmlns': 'http://www.gexf.net/1.2draft',
            'version': '1.2',
        })
        
        gexf.append(meta)
        gexf.append(graph)
        
        self.stdout.write("Writing...")
        
        options['output'].write(tostring(gexf, encoding="UTF-8"))
        options['output'].close()
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))