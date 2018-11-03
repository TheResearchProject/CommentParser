from collections import Counter
import cPickle
from multiprocessing import Pool, Process
import pdb
import os.path
import time

from nltk.tokenize import RegexpTokenizer
import networkx
import MySQLdb

from django.conf import settings
from django.db import connections

from comment_parser.utils import TextCleaner, dictfetch
from comment_parser.queryset_iterator import queryset_iterator    
from rss_parser.models import Algorithm, Comment, Newsitem, Result, Text
from rss_parser.mycommand import MyCommand

tokenizer = RegexpTokenizer(r'\w+')
text_cleaner = TextCleaner() 
        
def tokenize(item):
    clean_text = text_cleaner.clean(item.text.text)
    return item, tokenizer.tokenize(clean_text)       
    
def calculate(filename, graph, function):
    if not os.path.isfile(filename):
        print "Generating {}".format(filename)
        data = function(graph)
        print "Saving {}".format(filename)
        cPickle.dump(data, open(filename, 'wb'))     

class Command(MyCommand):
    help = 'Get summarized data from authors'
    items_used = "*"

    analysis_ins_query = """
        INSERT IGNORE INTO author_summary
            (author_id
            ,avg_nr_words 
            ,avg_wordlen 
            ,avg_words_gt6 
            ,avg_personal
            ,avg_collective 
            ,indegree
            ,indegree_centrality
            ,outdegree
            ,outdegree_centrality
            ,degree
            ,degree_centrality
            ,avg_shared
            ,nr_posts
            ,hub_score
            ,authority_score
            ,betweeness_centrality
            ,polarity_arousal
            ,polarity_valence) 
          VALUES ({})    
    """
    
    #def pbar_increment(self, dummy):
    #    super(Command, self).pbar_increment(self)
    
    def increment_counters(self, counter_list, key, amount = 1):
        for counter in counter_list:
            counter[key] += amount
            
    def get_newsitems_author_ids(self, newsitem_id):
        author_id_list = []
        query = """
            SELECT author_id FROM author_newsitem WHERE newsitem_id = %s            
        """
        cursor = connections[self.current_database].cursor()
        cursor.execute(query, [newsitem_id])
        for row in dictfetch(cursor):
            author_id_list.append(row['author_id'])      
        return author_id_list
    
    def work(self, item, tokenized_text):        
        if item.__class__ == Newsitem:
            author_id_list = self.get_newsitems_author_ids(item.id)
        else:      
            author_id_list = [item.author_id]   
            
        if len(author_id_list) == 0:   
            return item, False
               
        counters = []       
               
        for author_id in author_id_list:        
            if not author_id in self.author_data:
                counter = Counter()
                counters.append(counter)
                self.author_data[author_id] = {'name': author_id,
                                               'counter': counter,
                                               'texts_ids': [item.text.id]}
            else:
                counters.append(self.author_data[author_id]['counter'])
                self.author_data[author_id]['texts_ids'].append(item.text.id)
                
        if item.__class__ == Comment:
            if item.parent:
                parent_author = item.parent.author_id
                self.edges.append((author_id, parent_author))
            elif item.newsitem:
                newsitem_author_ids = self.get_newsitems_author_ids(item.newsitem.id)
                for newsitem_author_id in newsitem_author_ids:
                    self.edges.append((author_id, newsitem_author_id))
                
        last_word = None
        
        for word in tokenized_text:
            self.increment_counters(counters, 'total_wordcount')
            self.increment_counters(counters, 'total_wordlength', len(word))
            if len(word) > 6:
                self.increment_counters(counters, 'total_gt6words')
            if word in ["i", "mine", "me"]:
                self.increment_counters(counters, 'total_personal')
            if word in ['we', 'ours'] or (word == 'us' and last_word != 'the'): 
                self.increment_counters(counters, 'total_collective')
                
            last_word = word
        
        self.increment_counters(counters, 'author_postcount')    
        
        return item, True
        
    def divide_default_zero(self, num1, num2):
        try:
            return num1/num2
        except ZeroDivisionError:
            return 0
            
    def generate_author_data(self, database):
        self.author_data = {}
        for model in [Newsitem, Comment]:    
            
            if model == Newsitem:
                model_name = "Newsitem"
            else:
                model_name = "Comment"
                
            self.stdout.write("Processing model "+model_name)
        
            queryset = model.objects.using(database)\
                                    .filter(text__isnull=False)\
                                    .select_related('text__text')
                                    
            if model == Comment:
                queryset = queryset.select_related('newsitem__idauthor', 
                                                   'parent__authorid')
                                       
            self.pbar_setup(maxval=queryset.count())
            queryset_iter = queryset_iterator(queryset, chunksize=100)
            pool = Pool()   
            
                
            #pool.map_async(work, queryset_iter, callback=self.pbar_increment())
            
            #for item, tokenized in pool.imap_unordered(tokenize, queryset_iter, 100):
            for item in queryset_iter:
                item, tokenized = tokenize(item) 
                self.work(item, tokenized)
                
                self.pbar_increment()    
                
            self.pbar_destroy()        
            
    def create_graph(self, database):
        self.stdout.write("Creating NetworkX graph...")                
        
        graph = networkx.MultiDiGraph()       
                           
        self.stdout.write("Creating Nodes...")                
        for author in self.author_data:
            graph.add_node(author)
                        
        self.stdout.write("Creating Edges...")
        for edge in self.edges:     
            source_author, target_author = edge
            if target_author in graph:
                edge_data = graph.get_edge_data(source_author, 
                                                target_author)
                if edge_data:
                    edge_data[0]['weight'] += 1
                else:
                    graph.add_edge(source_author, 
                                   target_author, 
                                   weight=1)
                #endif            
            #endif        
        #endfor 

        self.stdout.write("Removing authors without edges...")
        #Excluding authors without edges
        self.authors_with_edges = set()
        for author in self.author_data:
            if len(graph[author]) > 0:
                self.authors_with_edges.add(author)
            
        for author in set(self.author_data.keys()) - self.authors_with_edges:
            graph.remove_node(author)    
            
        return graph
        
    def load_or_calculate(self, filename, graph, function):
        if os.path.isfile(filename):
            self.stdout.write("Loading {}".format(filename))
            return cPickle.load(open(filename, 'rb'))
        else:
            self.stdout.write("Generating {}".format(filename))
            data = function(graph)
            self.stdout.write("Saving {}".format(filename))
            cPickle.dump(data, open(filename, 'wb'))     
            return data
            
    def handle(self, *args, **options):        
        self.stdout.write('Command started') 
        super(Command, self).handle(self, *args, **options)
        
        self.edges = []
        
        for database in self.selected_dbs:       
            self.current_database = database
            
            self.stdout.write("Processing database "+database)
            targetdb_cursor = connections[database].cursor()
            
            self.stdout.write("Truncating (deleting all rows) from target table")
            targetdb_cursor.execute("TRUNCATE TABLE author_summary")
            
            algorithm_anew_valence, _ = Algorithm.objects.using(database)\
                                    .get_or_create(name="anew_valence")
            algorithm_anew_arousal, _ = Algorithm.objects.using(database)\
                                                .get_or_create(name="anew_arousal")
     
            author_data_filename = "{}_author_data".format(database)   
            if os.path.isfile(author_data_filename):
                self.stdout.write("Loading generated author data")
                self.author_data = cPickle.load(open(author_data_filename, 'rb'))
            else:
                self.stdout.write("Generating author data")
                self.generate_author_data(database)
                self.stdout.write("Saving generated author data")
                cPickle.dump(self.author_data, open(author_data_filename, 'wb'))     
     
            graph_filename = "{}_graph".format(database)   
            if os.path.isfile(graph_filename):
                self.stdout.write("Loading previously processed graph")
                graph = networkx.read_gpickle(graph_filename)
            else:
                self.stdout.write("Generating graph")
                graph = self.create_graph(database)
                self.stdout.write("Saving graph")
                networkx.write_gpickle(graph, graph_filename)
                
            self.stdout.write("Generating polarity")    
            #polarity
            texts = []
            for author in graph:
                for text_id in self.author_data[author]['texts_ids']:
                    texts.append(text_id)
            #polarity_arousal
            polarity_arousal = {}
            results = Result.objects.using(database).filter(
                algorithm=algorithm_anew_arousal,
                text_id__in=texts)
            for result in results:
                polarity_arousal[result.text_id] = float(result.value)  
            #polarity_valence
            polarity_valence = {}
            results = Result.objects.using(database).filter(
                algorithm=algorithm_anew_valence,
                text_id__in=texts)
            for result in results:
                polarity_valence[result.text_id] = float(result.value)                  
                
            #Indegree
            indegree = self.load_or_calculate(
                                      '{}_indegree'.format(database), 
                                      graph,
                                      graph.in_degree)
            indegree_centrality = self.load_or_calculate(
                                      '{}_indegree_centrality'.format(database), 
                                      graph,
                                      networkx.in_degree_centrality)            
            #Outdegree
            outdegree = self.load_or_calculate(
                                     '{}_outdegree'.format(database), 
                                     graph,
                                     graph.out_degree)             
            outdegree_centrality = self.load_or_calculate(
                                     '{}_outdegree_centrality'.format(database), 
                                     graph,
                                     networkx.out_degree_centrality)            
            #Degree
            degree = self.load_or_calculate(
                                        '{}_degree'.format(database), 
                                        graph,
                                        graph.degree)            
            degree_centrality = self.load_or_calculate(
                                        '{}_degree_centrality'.format(database), 
                                        graph,
                                        networkx.degree_centrality)
            #Page rank person
            #pagerank = networkx.pagerank(graph)
            #Page rank person(weighted)
            #pagerank = networkx.pagerank(graph)
            
            hits = self.load_or_calculate('{}_hits'.format(database), 
                                              graph,
                                              networkx.hits_scipy)
            #hub score person
            hubs = hits[0]
            #authority score
            authorities = hits[1]
            
            #print "Starting Betweeness and Closeness in parallel"
            #betweeness_process = Process(
            #    target=calculate,
            #    args=('{}_betweeness_centrality'.format(database), 
            #          graph,
            #          networkx.betweenness_centrality
            #    ))   
            #betweeness_process.start()
            #
            #closeness_process = Process(
            #    target=calculate,
            #    args=('{}_closeness_centrality'.format(database), 
            #          graph,
            #          networkx.closeness_centrality))
            #closeness_process.start()
            #
            #print "Checking if processes are alive every 120 seconds"
            #betweeness_done = False
            #closeness_done = False
            #while True:
            #    if not betweeness_done and not betweeness_process.is_alive():
            #        print "Betweeness done"
            #        betweeness_done = True
            #    if not closeness_done and not closeness_process.is_alive():
            #        print "Closeness done"
            #        closeness_done = True
            #    if betweeness_done and closeness_done:
            #        break
            #    time.sleep(120)
            #    
            #print "Both done, reading results from disk"
                
            #betweenness
            betweenness_centrality = self.load_or_calculate(
                                    '{}_betweeness_centrality'.format(database), 
                                    graph,
                                    networkx.betweenness_centrality)
            #closeness
            closeness_centrality = self.load_or_calculate(
                                     '{}_closeness_centrality'.format(database), 
                                     graph,
                                     networkx.closeness_centrality)
            #clustering coefficietn
            #clustering = networkx.clustering(graph)
            #eccentricity
            #self.stdout.write("Calculating Eccentricity...")
            #eccentricity = networkx.eccentricity(graph)
            
            formatted_query = self.analysis_ins_query.format(
                ",".join(["%s" for i in range(19)])    
            )
            
            self.stdout.write("Inserting data at target table")
            
            self.pbar_setup(maxval=len(graph))
            
            insert_data = []
            
            for author in graph:
                counter = self.author_data[author]['counter']
                #create a row in the target table for each author data
                params = []
                #`author`
                params.append(author)
                #,`newssite`    
                #params.append(database)
                #,`avg_nr_words` 
                params.append(self.divide_default_zero(float(counter['total_wordcount']), 
                                                       float(counter['author_postcount'])))
                #,`avg_wordlen` 
                params.append(self.divide_default_zero(float(counter['total_wordlength']), 
                                                       float(counter['total_wordcount'])))
                #,`avg_words_gt6` 
                params.append(self.divide_default_zero(float(counter['total_gt6words']), 
                                                       float(counter['total_wordcount'])))
                #,`avg_personal`
                params.append(self.divide_default_zero(float(counter['total_personal']), 
                                                       float(counter['total_wordcount'])))
                #,`avg_collective`  
                params.append(self.divide_default_zero(float(counter['total_collective']), 
                                                       float(counter['total_wordcount'])))
                #,`indegree`
                params.append(indegree[author])
                params.append(indegree_centrality[author])
                #,`outdegree`
                params.append(outdegree[author])
                params.append(outdegree_centrality[author])
                #,`degree`
                params.append(degree[author])
                params.append(degree_centrality[author])
                #,`avg_shared`
                params.append(0)
                #,`pagerank`
                #params.append(indegree[author])  
                #,`pagerank_weighted`
                #params.append(indegree[author])
                #,`nr_posts`
                params.append(counter['author_postcount'])
                #,`hub_score`
                params.append(hubs[author])
                #,`indegree[author]ity_score`
                params.append(authorities[author])
                #,`betweeness`
                params.append(betweenness_centrality[author])
                #,`closeness`
                #params.append(closeness_centrality[author])
                #,`clustering_coef`
                #params.append(indegree[author])
                #,`eccentricity`
                #params.append(eccentricity[author])
                #,`constraint`
                #params.append(author)
                
                #polarity
                total_arousal = 0
                total_valence = 0
                qty_texts = 0
                for text_id in self.author_data[author]['texts_ids']:
                    if text_id in polarity_arousal:
                        total_arousal += polarity_arousal[text_id]
                    if text_id in polarity_valence:
                        total_valence += polarity_valence[text_id]
                    qty_texts += 1
                #,`polarity_arousal`                
                params.append(float(total_arousal)/float(qty_texts))
                #,`polarity_valence`                
                params.append(float(total_valence)/float(qty_texts))
                
                insert_data.append(params)
                
                if len(insert_data) >= 50:
                    targetdb_cursor.executemany(formatted_query, insert_data)
                    insert_data = []
                
                self.pbar_increment()    
            self.pbar_destroy()
            
            if len(insert_data) > 0:
                targetdb_cursor.executemany(formatted_query, insert_data)

        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
