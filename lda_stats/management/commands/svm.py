import pdb
import sys

from rss_parser.mycommand import MyCommand

from rss_parser.models import Newsitem, Algorithm, Result

from comment_parser.queryset_iterator import queryset_iterator

import lda_stats.utils.idf as utils

from sklearn import svm

class Command(MyCommand):
    help = ''
    
    def handle(self, *args, **options):
        super(Command, self).handle(self, *args, **options)
        
        k = 5
        
        print "Reading data to memory"

        TFIDF_list=[]
        label=[]
        
        queryset = Newsitem.objects.all()
        self.pbar_setup(maxval=queryset.count())
        newsitems = queryset_iterator(queryset, chunksize=100)
        
        for newsitem in newsitems:
            TFIDF_list.append(utils.TFIDF(utils.tokenize(newsitem.text.text)))
            if newsitem.cat1 in [1, 2] :
                label.append(1)
            else:
                label.append(0)
            self.pbar_increment()
            
        self.pbar_destroy()
        
        print "Training..."
        
        TFIDF_svm=[]
        for i in TFIDF_list:
            TFIDF_svm.append(utils.TFIDF_to_list(i))
        # TFIDF_svm is the input matrix of SVM
        
        # Reads the train_len from command line
        #train_len=int(sys.argv[1])
        train_len=200
        
        # Index of train samples from class 0
        indexZero=[i for i in range(len(label)) if label[i]==0][:train_len]
        # Index of train samples from class 1
        indexOne=[i for i in range(len(label)) if label[i]==1][:train_len]
        # We have K number of positive samples and also K number of negative samples
        
        train=[]
        train_label=[]
        for  i in indexZero+indexOne:
            train.append(TFIDF_svm[i])
            train_label.append(label[i])
        # Train: train matrix
        # train_label: lables of train data
        
        # The other samples are test samples.
        test = [TFIDF_svm[i] for i in range(len(TFIDF_svm)) if i not in indexZero+indexOne]
        test_label = [label[i] for i in range(len(label)) if i not in indexZero+indexOne]
        
        
        clf = svm.SVC()
        # Train the model
        clf.fit(train, train_label)        
        
        counter1=0
        TP=0
        TN=0
        FP=0
        FN=0
        
        print "Estimating..."
        self.pbar_setup(maxval=len(test))
        
        for i in test:
            estimate_label=clf.predict([i])[0]
            if estimate_label==1 and label[counter1]==1:
                TP+=1
            elif estimate_label==1 and label[counter1]==0:
                FN+=1
            elif estimate_label==0 and label[counter1]==0:
                TN+=1
            else:
                FP+=1
            counter1+=1
            self.pbar_increment()
            
        self.pbar_destroy()
        
        print 'TP=>',TP , 'FN=>',FN, 'FP=>',FP,'TN=>', TN    
        #print 'F1 Measurement: ', float(TP+TN)/(TP+FN+FP+TN), float(TP)/(TP+FP), float(TP)/(TP+FN), TP, FN, FP, TN

        data = [
            ('algo_svm_tp', TP),
            ('algo_svm_fn', FN),
            ('algo_svm_fp', FP),
            ('algo_svm_tn', TN),
            ('algo_svm_score', clf.score(train, train_label)),
        ]
            
        print "Saving algorithm results"    
            
        for item in data:
            algorithm_name = item[0]
            value = item[1]
            algorithm, create = Algorithm.objects.get_or_create(name=algorithm_name)
            result, create = Result.objects.get_or_create(algorithm=algorithm)
            result.value=str(value)
            result.save() 
        
        algo_svm_estimative, create = Algorithm.objects.get_or_create(name="algo_svm_estimative")
        
        print "Calculating estimatives and saving result"
        
        queryset = Newsitem.objects
        self.pbar_setup(maxval=queryset.count())
        newsitems = queryset_iterator(queryset.all(),chunksize=100)
        
        for newsitem in newsitems:
            estimate=clf.predict([utils.TFIDF_to_list(utils.TFIDF(utils.tokenize(newsitem.text.text)))])        
            Result.objects.create(algorithm=algo_svm_estimative,
                                  text=newsitem.text,
                                  value=str(estimate[0]))
            self.pbar_increment()

        self.pbar_destroy()            
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
