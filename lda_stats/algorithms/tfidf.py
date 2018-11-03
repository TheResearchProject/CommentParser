import re,math

all_idfs = None
stopwords = []

def getIDF(word):
    global all_idfs
    fileName = "enidf.txt"
    if not all_idfs:
        all_idfs = {}
        f = open(fileName, 'r')
        for line in f.readlines():
            m=re.match('(.+)\s(\d+)', line)
            all_idfs[m.group(1).lower()] = float(m.group(2))
    word = word.lower()
    if word in all_idfs:
        return all_idfs[word]
    return False

def getTFIDFArray(lines):
    global stopwords
    if not stopwords:
        stopwords = []
        ll = open("stopwords.txt").readlines()
        for l in ll:
            stopwords.append(l.strip())
    n = 110151172.000
    tfs = {}
    dels = "#,\"\'.?!;:|0123456789@()-"
    for line in lines:
        l = line.lower().strip()
        l = re.sub("http://\S*\s", "", l)
        l = re.sub("http://\S$", "", l)
        for d in dels:
            l = l.replace(d," ")
            list = l.strip().split()
            for w in list:
                if w in tfs: 
                    tfs[w]+=1
                else: 
                    tfs[w]=1
                    
    ret_tfs = {}                
    for key, value in tfs.items():
        if key not in stopwords:
            idf = getIDF(key)
            if idf:
                ret_tfs[key] = value*math.log(n/(idf+1.000), 2)
    return ret_tfs

def getSim(tfidf1, tfidf2):
    p1 = 0
    p2 = 0
    p12 = 0
    for w in tfidf1.keys():
        p1 += tfidf1[w]**2
        if tfidf2.has_key(w):
            p12 += tfidf1[w]*tfidf2[w]
    for w in tfidf2.keys():
        p2 += tfidf2[w]**2
    if not p1 or not p2:
        return 0
    return p12/(math.sqrt(p1)*math.sqrt(p2))
