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
        
        authors = set()
        
        self.stdout.write("Processing NewsItems")
        
        queryset = Newsitem.objects.using(selected_db).only('id').all()
        self.pbar_setup(maxval=queryset.count())
        
        for newsitem in queryset_iterator(queryset, chunksize=10000):
            author_id = "A{}".format(newsitem.idauthor) 
            nodes.append(Element('node', attrib={
                'id': author_id,                                           
                'label': "Author {}".format(newsitem.idauthor),
            }))
            authors.add(author_id)
            
            self.pbar_increment()
    
        self.pbar_destroy()       
        
        self.stdout.write("Processing Comments")
        
        queryset = Comment.objects.using(selected_db)\
                                  .all()
        edge_id = 0
        self.pbar_setup(maxval=queryset.count())
        
        for comment in queryset_iterator(queryset, chunksize=10000):
            author_id = "A{}".format(comment.authorid) 
            if not author_id in authors:
                nodes.append(Element('node', attrib={
                    'id': author_id,
                    'label': "Author {}".format(comment.authorid),
                }))
                authors.add(author_id)
            
            if comment.parent_id:
                target_id = author_id
            else:
                try:
                    target_id = "A{}".format(comment.newsitem.idauthor)
                except Newsitem.DoesNotExist:
                    continue
                
            edges.append(Element('edge', attrib={
                'id': str(edge_id),
                'source': author_id,
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