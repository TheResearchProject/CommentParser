import pdb
import sys

import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.metrics import roc_curve, auc

from rss_parser.mycommand import MyCommand
from rss_parser.models import Newsitem, Algorithm, Result
from comment_parser.queryset_iterator import queryset_iterator
import lda_stats.utils.idf as utils

class Command(MyCommand):
    help = ''
    
    def handle(self, *args, **options):
        
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
        
        print "Creating traing and test data..."
        
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
        
        print "Fitting..."
        clf = svm.SVC(probability=True)
        # Train the model
        clf.fit(train, train_label)        
        
        #print "Score: " + clf.score(train, train_label)    
        
        print "Generating probabilities"
        pred_probas = clf.predict_proba(test)[:,1]

        fpr,tpr,_ = roc_curve(test_label, pred_probas)
        roc_auc = auc(fpr,tpr)
        
        print "Plotting..."
        plt.plot(fpr,tpr,label='area = %.2f' %roc_auc)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.legend(loc='lower right')
        
        print "Saving!"
        plt.savefig('out.png')
            
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
