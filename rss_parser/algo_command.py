import pdb

from rss_parser.mycommand import MyCommand

from rss_parser.models import Newsitem, Algorithm, Result

from comment_parser.queryset_iterator import queryset_iterator

import lda_stats.utils.idf as utils

class AlgoCommand(MyCommand):
    help = ''
    algo_name = 'knn_uniform'
    
    def handle(self, *args, **options):
        
        TFIDF_list=[]
        label=[]
        
        queryset = Newsitem.objects
        self.pbar_setup(maxval=queryset.count())
        newsitems = queryset_iterator(queryset.all(),chunksize=100)
        
        for newsitem in newsitems:
            TFIDF_list.append(self.tokenize(newsitem.text.text))
            if newsitem.cat1 in [1, 2] :
                label.append(1)
            else:
                label.append(0)
            self.pbar_increment()
            
        self.pbar_destroy()
        
        self.train()
        
        print "Estimating..."
        self.pbar_setup(maxval=len(TFIDF_list))        
        
        counter1=0
        TP=0
        TN=0
        FP=0
        FN=0
        while counter1 < len(TFIDF_list):
            distance_list=[]
            counter2=0
            while counter2< len(TFIDF_list):
                if counter1 !=counter2:
                    distance_list.append(utils.TFIDF_distance(TFIDF_list[counter1], TFIDF_list[counter2]))
                counter2+=1
            nearest_list=sorted(range(len(distance_list)), key=lambda i:distance_list[i])[:k]
            repeat_dic={}
            for i in  nearest_list:
                if repeat_dic.has_key(label[i]):
                    repeat_dic[label[i]]+=1
                else:
                    repeat_dic[label[i]]=1
            estimate_label=max(repeat_dic, key=repeat_dic.get)
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
            
        data = [
            ('algo_knn_tp', TP),
            ('algo_knn_fn', FN),
            ('algo_knn_fp', FP),
            ('algo_knn_tn', TN),
        ]
        
        print 'TP=>',TP , 'FN=>',FN, 'FP=>',FP,'TN=>', TN    
        #print 'F1 Measurement: ', float(TP+TN)/(TP+FN+FP+TN), float(TP)/(TP+FP), float(TP)/(TP+FN), TP, FN, FP, TN
        
        print "Saving algorithm results"    
        
        for item in data:
            algorithm_name = item[0]
            value = item[1]  
            algorithm, create = Algorithm.objects.get_or_create(name=algorithm_name)
            result, created = Result.objects.get_or_create(algorithm=algorithm)
            result.value=str(value)
            result.save() 
        
        algo_knn_uniform_estimative, create = Algorithm.objects.get_or_create(name="algo_knn_uniform_estimative")
        
        print "Calculating estimatives and saving result"
        
        queryset = Newsitem.objects
        self.pbar_setup(maxval=queryset.count())
        newsitems = queryset_iterator(queryset.all(),chunksize=100)
        
        for newsitem in newsitems:
            data=utils.TFIDF(utils.tokenize(row[0]))
            distance_list=[]
            for i in  range(len(TFIDF_list)):
                distance_list.append(utils.TFIDF_distance(data, TFIDF_list[i]))
            nearest_list=sorted(range(len(distance_list)), key=lambda i:distance_list[i])[:k]
            repeat_dic={}
            for i in  nearest_list:
                if distance_list[i] !=0:
                    if repeat_dic.has_key(label[i]):
                        repeat_dic[label[i]]+=1
                    else:
                        repeat_dic[label[i]]=1
            estimate=max(repeat_dic, key=repeat_dic.get)            
            Result.objects.create(algorithm=algo_knn_uniform_estimative,
                                  text=newsitem.text,
                                  value=str(estimate))
            self.pbar_increment()

        self.pbar_destroy()            
        
        self.stdout.write(self.style.SUCCESS('Command executed succesfully'))
        
    def tokenize(self, text):
        return utils.TFIDF(utils.tokenize(text))

    def train(self):
        pass
    
    def estimate(self, item):
        pass
    
    
