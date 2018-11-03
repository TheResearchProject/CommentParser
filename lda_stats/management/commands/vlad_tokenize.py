import cPickle
import pdb
import re

import nltk
from nltk.stem.wordnet import WordNetLemmatizer

from django.db import connections,transaction
from django.db.utils import IntegrityError

from rss_parser.mycommand import MyCommand

from rss_parser.models import Comment, Word, Algorithm, Result

from comment_parser.queryset_iterator import queryset_iterator

def save_word(word_data, text_list):
    print word_data
    try:
        word = Word.objects.create(**word_data)
    except IntegrityError:
        pdb.set_trace()    
    word.texts.set(text_list)    

class WordCache():
    def __init__(self):
        self.words = {}
        self.current_id = 1
            
    def get(self, word):
        return self.words[word]['id'] if word in self.words else None
        
    def save(self, word_data):
        word_data['id'] = self.current_id
        self.current_id += 1
        self.words[word_data['word']] = word_data
        return word_data['id']
        
    def get_as_list(self):
        word_list = [v for k,v in self.words.iteritems()]
        return word_list

class Command(MyCommand):
    help = 'Gets the tokens for every text (comment or newsitem)'
    
    url1_regex = re.compile('(http|https|ftp|mailto|tel):\S+[/a-zA-Z0-9]')
    url2_regex = re.compile('\w{3,}\.[\S/a-zA-Z0-9]+')
    punctuation_regex = re.compile('[^\w\s\']')
    spaces_regex = re.compile('\s{2,}')
    
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--reset', action='store_true')  
        
    def clean_text(self, text):
        new_text = self.url1_regex.sub(' ',text.lower())
        new_text = self.url2_regex.sub(' ',new_text)
        new_text = self.punctuation_regex.sub(' ',new_text)
        new_text = self.spaces_regex.sub(' ',new_text)
        return new_text
        
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        lem = WordNetLemmatizer()

        stopwords = {}
        with open('stopwords.txt', 'rU') as f:
            for line in f:
                stopwords[line.strip()] = 1

        for database in self.selected_dbs:    
            
            print "Processing database " + database

            algorithm_tokenize, created = Algorithm.objects.using(database).get_or_create(
                                                               name="vlad_tokenize")
    
            word_cache = WordCache()
    
            print "Excluding previous results"
            #Exclude all tokens and create them again
            Result.objects.using(database).filter(algorithm=algorithm_tokenize).delete()
            Word.objects.using(database).all().delete()
            print "Reading comments"
            non_tokenized_comments = Comment.objects.using(database).filter(text__isnull=False)
            total_comments = non_tokenized_comments.count()
            if total_comments == 0:
                print "No items to tokenize!"
                return   
            comments = queryset_iterator(non_tokenized_comments.all(),chunksize=100)
            
            text_word = []
            
            print "Startint process!"
            self.pbar_setup(maxval=total_comments)
            
            for comment in comments:
                tokens = nltk.word_tokenize(self.clean_text(comment.text.text))
                text = [word for word in tokens if word not in stopwords]
                tagged_text = nltk.pos_tag(text)
        
                for word_text, tag in tagged_text:
                    if tag in ['NN','NNS']:
                        word_id = word_cache.get(word_text)
                        if not word_id:
                            word_attributes = {
                                'word': word_text, 
                                'tag': tag,
                                'noun': lem.lemmatize(word_text)
                            }
                            word_id = word_cache.save(word_attributes)
                        text_word.append((word_id, comment.text.id))
                                
                self.pbar_increment()
                
            self.pbar_destroy()
            
            print "Bulk creating words"
            Word.objects.using(database).bulk_create([Word(**attrib) for attrib in word_cache.get_as_list()])
            
            print "Opening cursor"
            cursor = connections[database].cursor()   
            query = 'INSERT IGNORE INTO word_texts (word_id, text_id) VALUES (%s, %s)'
            
            print "Inserting rows for relation word-text..."
            self.pbar_setup(maxval=len(text_word))
            while len(text_word) > 0:
                chunk = []
                while len(chunk) < 10000:
                    try:
                        chunk.append(text_word.pop())
                        self.pbar_increment()
                    except IndexError:
                        break
                    
                cursor.executemany(query,chunk)
                transaction.commit(database)
                
            self.pbar_destroy()    
    
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
