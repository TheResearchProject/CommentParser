import datetime

import networkx

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

from rss_parser.models import Newsitem, Comment

# Create your views here.
def index(request):
    context = {
        'databases':settings.AVAILABLE_DATABASES,
        'database':settings.AVAILABLE_DATABASES[0],
    }
    return render(request, 'netvis/index.html', context)

def get_data(newsitem_id=None, 
             date_from=None, 
             date_to=None, 
             strip_by_date=False, 
             database=settings.AVAILABLE_DATABASES[0]):
    # init vars
    nodes=[]
    links=[]
    node_index={}       
        
    newsitems_queryset = Newsitem.objects.using(database)
    if newsitem_id:
        newsitems_queryset = [newsitems_queryset.get(pk=newsitem_id)]
    else:
        if date_from:
            newsitems_queryset = newsitems_queryset.filter(date__gte=date_from)
        if date_to:
            newsitems_queryset = newsitems_queryset.filter(date__lte=date_to)   
            
    for newsitem in newsitems_queryset:
        node_index_key='N%d'%newsitem.id
        if node_index_key not in node_index:
            nodes.append({'type': 'n', 
                          'id': newsitem.id, 
                          'title': newsitem.title, 
                          'author': newsitem.idauthor, 
                          'date': newsitem.date, 
                          'wc': newsitem.text.wordcount if newsitem.text else 0})
            node_index[node_index_key]=len(nodes)-1
        else:
            index=node_index[node_index_key]
            node=nodes[index]
            node['author']+=', '+newsitem.author        
    
    comments_queryset = Comment.objects.using(database)
    if newsitem_id:
        comments_queryset = comments_queryset.filter(newsitem_id=newsitem_id)
    else:
        if date_from:
            comments_queryset = comments_queryset.filter(date__gte=date_from)
        if date_to:
            comments_queryset = comments_queryset.filter(date__lte=date_to)
            
    comments = comments_queryset.all()            
    
    for comment in comments:
        nodes.append({'type': 'c', 
                      'id': comment.id, 
                      'title': "", 
                      'date': comment.date, 
                      'author': comment.authorid, 
                      'wc': comment.text.wordcount})
        node_index['C%s'%comment.id]=len(nodes)-1
        
    for comment in comments:      
        try:
            source=node_index['C%s'%comment.id]
            if comment.parent:
                target=node_index['%s%s'%('C', comment.parent_id)]
            else:
                target=node_index['%s%s'%('N', comment.newsitem_id)]
            links.append({'source': source, 'target': target, 'date': comment.date})
        except KeyError:
            pass    
        
    return nodes, links
    
    
def data(request):
    
    newsitem=request.GET.get('newsitem', None)
    date_from_text = request.GET.get('date_from', None)
    if date_from_text:
        date_from = datetime.datetime.strptime(date_from_text, '%d-%m-%Y')
    else:
        date_from = None
    date_to_text=request.GET.get('date_to', None)
    if date_to_text:
        date_to = datetime.datetime.strptime(date_to_text, '%d-%m-%Y')
    else:
        date_to = None
    strip_by_date = True if request.GET.get('strip_by_date') == 'true' else False
    if newsitem==None and (date_from==None or date_to==None):
        return json.dumps({'_type': 'error', 'message': 'invalid parameters'}) 

    nodes, links = get_data(newsitem_id=newsitem,
                            date_from=date_from, 
                            date_to=date_to)
        
    return JsonResponse({'nodes': nodes, 'links': links})
    
def graphinfo(request):
    # check params
    id1=request.GET.get('id1', None)
    if id1==None or len(id1)==0 or id1[0].lower() not in ('n', 'c'):
        return JsonResponse({'_type': 'error', 'message': 'invalid parameters'})

    # retrieve id of newsitem
    id_type=id1[0].lower()
    id_val=id1[1:]    
    
    if id_type=='n':
        newsitem_id=id_val
    else:
        comment = Comment.objects.get(pk=id_val)
        if not comment:
            return JsonResponse({'_type': 'error', 'message': 'comment not fount'})
        newsitem_id = comment.newsitem_id
    
    nodes, links = get_data(newsitem_id=newsitem_id)
    
    if len(nodes)==0 or nodes[0]['type']!='n':
        return json.dumps({'_type': 'error', 'message': 'newsitem not found correctly'})

    # create networkx graph
    g=networkx.Graph()
    g.add_nodes_from(range(len(nodes)))
    g.add_edges_from([(i['source'], i['target']) for i in links])

    # find index of id1 in nodes
    ni=0 if id_type=='n' else map(lambda n: n['id'], nodes).index(id_val, 1)

    if g.number_of_edges()==0:
        diameter = 0
    else:
        diameter = networkx.diameter(g)
        
    # make result
    res={
        'newsitem': newsitem_id,
        'diameter': 0 if g.number_of_edges()==0 else networkx.diameter(g),
        'avg_shortest_path': 0 if g.number_of_edges()==0 else '%0.2f'%networkx.average_shortest_path_length(g),
        'avg_clustering': networkx.average_clustering(g),
        'distance': networkx.shortest_path_length(g, 0, ni),
        'degree': g.degree(ni),
    }
    
    # return json
    return JsonResponse(res)    
