class Stopwords():
    def __init__(self, stopword_file):
        self.stopwords = [w.strip() for w in open(stopword_file).readlines()]
        
    def is_stopword(self, word):
        return word.lower() in self.stopwords