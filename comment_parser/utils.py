import re
from HTMLParser import HTMLParser 

class TextCleaner():
    def __init__(self):
        self.html_parser = HTMLParser()

    def clean(self, text):
        text = self.html_parser.unescape(text)
        text = re.sub('@[\w_]+','',text)
        text = re.sub('(https?://[\w\.\/\?&=]+)\s?','',text)
        text = re.sub('[^\w\s#_\']',' ',text)
        text = re.sub('\s{2,9999}',' ',text)
        return text.lower()
        
def dictfetch(cursor, arraysize = 1000):
    "Return all rows from a cursor as a dict"    
    columns = [col[0] for col in cursor.description]
    
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield dict(zip(columns, result))
        