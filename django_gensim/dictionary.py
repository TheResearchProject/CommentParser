import pdb
from collections import defaultdict

from gensim.corpora import Dictionary as GensimDictionary
from six import iteritems, itervalues, string_types

from django.db import transaction, IntegrityError

from .models import Word
from .models import Dictionary as DictionaryModel


class DummyDict():
    def __init__(self, dictionary):
        self.dictionary = dictionary
        
    def __len__(self):                                   
        return Word.objects.filter(dictionary=self.dictionary).count()      
        
    #def has_key(self, key):
    #    return self.__contains__(key)
        
    def itervalues(self):
        return self.values()        
        
    def __eq__(self, compare_to):
        for key in compare_to:
            if not key in self or self[key] != compare_to[key]:
                return False
        return True       
        
    def __iter__(self):
        return self.iteritems()
        
    def get(self, key, default=None):
        if not key in self:
            if default != None:
                return default
            else:
                raise KeyError(key)
        else:
            return self.__getitem__(key)
               
class Token2ID(DummyDict): 
    def __getitem__(self, key):         
        word = Word.objects.filter(word=key, dictionary=self.dictionary).first()
        if not word:
            raise KeyError(key)
        return word.sequence
                                                   
    def __setitem__(self, key, item):
        try:
            Word.objects.create(sequence=item, word=key, dictionary=self.dictionary)
        except IntegrityError:
            pass   
        
    def __contains__(self, key):
        word = Word.objects.filter(word=key, dictionary=self.dictionary).first()
        return True if word else False
        
    def values(self):
        return [word.sequence for word in self.dictionary.word_set.all()]  
        
    def keys(self):
        return [word.word for word in self.dictionary.word_set.all()]   
        
    def iteritems(self):
        for word in self.dictionary.word_set.all():
            yield (word.word, word.sequence)    
        
class ID2Token(DummyDict):        
    def __getitem__(self, key):         
        word = Word.objects.filter(sequence=key, dictionary=self.dictionary).first()
        if not word:
            raise KeyError(key)
        return word.word
                                                   
    def __setitem__(self, key, item):
        try:
            Word.objects.create(sequence=key, word=item, dictionary=self.dictionary)
        except IntegrityError:
            pass   
        
    def __contains__(self, key):
        word = Word.objects.filter(sequence=key, dictionary=self.dictionary).first()
        return True if word else False     
        
    def values(self):
        return [word.word for word in self.dictionary.word_set.all()]  
        
    def keys(self):
        return [word.sequence for word in self.dictionary.word_set.all()]
        
    def iteritems(self):
        for word in self.dictionary.word_set.all():
            yield (word.sequence, word.word)         
        
class DFS(DummyDict):        
    def __getitem__(self, key):         
        word = Word.objects.filter(sequence=key, dictionary=self.dictionary).first()
        if not word:
            raise KeyError(key)
        return word.amount_of_documents
                                                   
    def __setitem__(self, key, item):
        try:
            word = Word.objects.filter(sequence=key, dictionary=self.dictionary).first()
            word.amount_of_documents = item
            word.save()
        except IntegrityError:
            pass   
        
    def __contains__(self, key):
        word = Word.objects.filter(sequence=key, dictionary=self.dictionary).first()
        return True if word else False     
        
    def values(self):
        return [word.amount_of_documents for word in self.dictionary.word_set.all()]  
        
    def keys(self):
        return [word.sequence for word in self.dictionary.word_set.all()]
        
    def iteritems(self):
        for word in self.dictionary.word_set.all():
            yield (word.sequence, word.amount_of_documents)          
    
        
class Dictionary(GensimDictionary):   
    def __init__(self, documents=None, prune_at=2000000):        
        """
        If `documents` are given, use them to initialize Dictionary (see `add_documents()`).
        """
        self.dictionary_model = DictionaryModel()
        self.dictionary_model.save()
        self.token2id = Token2ID(self.dictionary_model)  # token -> tokenId
        self.id2token = ID2Token(self.dictionary_model)  # reverse mapping for token2id; only formed on request, to save memory
        self.dfs = DFS(self.dictionary_model)  # document frequencies: tokenId -> in how many documents this token appeared

        self.num_docs = 0  # number of documents processed
        self.num_pos = 0  # total number of corpus positions
        self.num_nnz = 0  # total number of non-zeroes in the BOW matrix
        
        self.current_sequence = 0

        #pdb.set_trace()
        if documents is not None:
            self.add_documents(documents, prune_at=prune_at)         
            
    def __getitem__(self, key):     
        return self.id2token[key]            
        
    def __str__(self):
        some_keys = "[{0}]".format(", ".join(
            [word.word for word in Word.objects.all()[:5]]))
        return "Dictionary(%i unique tokens: %s%s)" % (len(self), some_keys, '...' if len(self) > 5 else '')
        
    def filter_tokens(self, bad_ids=None, good_ids=None):
        """                                                                      
        Remove the selected `bad_ids` tokens from all dictionary mappings, or, keep
        selected `good_ids` in the mapping and remove the rest.
        `bad_ids` and `good_ids` are collections of word ids to be removed.
        """
        if bad_ids is not None:
            bad_ids = set(bad_ids)
            Word.objects.filter(sequence__in=bad_ids).delete()
        if good_ids is not None:                                                  
            good_ids = set(good_ids)
            Word.objects.exclude(sequence__in=good_ids).delete()
                                                                                  
        self.compactify()        
        
    def compactify(self):
        self.current_sequence = 0
        for word in Word.objects.order_by('sequence'):
            #print "current_sequence = {0} -=- word: {1} -=- word_id = {2}".format(
            #    current_sequence, word.word, word.id)
            word.sequence = self.current_sequence
            word.save()
            self.current_sequence += 1
            
    def doc2bow(self, document, allow_update=False, return_missing=False):
        """
        Convert `document` (a list of words) into the bag-of-words format = list
        of `(token_id, token_count)` 2-tuples. Each word is assumed to be a
        **tokenized and normalized** string (either unicode or utf8-encoded). No further preprocessing
        is done on the words in `document`; apply tokenization, stemming etc. before
        calling this method.
        If `allow_update` is set, then also update dictionary in the process: create
        ids for new words. At the same time, update document frequencies -- for
        each word appearing in this document, increase its document frequency (`self.dfs`)
        by one.
        If `allow_update` is **not** set, this function is `const`, aka read-only.
        """
        if isinstance(document, string_types):
            raise TypeError("doc2bow expects an array of unicode tokens on input, not a single string")

        # Construct (word, frequency) mapping.
        counter = defaultdict(int)
        for w in document:
            counter[w if isinstance(w, unicode) else unicode(w, 'utf-8')] += 1
        
        if return_missing:
            missing = dict((w, freq) for w, freq in iteritems(counter) if w not in token2id)
            
        if allow_update:
            for word_text, frequency in iteritems(counter):
                word, created = Word.objects.get_or_create(
                    dictionary=self.dictionary_model,
                    word=word_text)
                if created:
                    word.sequence = self.current_sequence
                    self.current_sequence += 1
                    word.save()
                else:
                    word.amount_of_documents += 1
                    word.save()
                    
                

    
        results = dict((self.token2id[w], freq) for w, freq in iteritems(counter) if w in self.token2id)

        if allow_update:
            self.num_docs += 1
            self.num_pos += sum(itervalues(counter))
            self.num_nnz += len(results)

        # return tokenids, in ascending id order
        results = sorted(iteritems(results))
        if return_missing:
            return results, missing
        else:
            return results            
            