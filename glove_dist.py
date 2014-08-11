#!/usr/bin/python
# -*- coding: utf-8 -*-

# author  : eclipse
# email   : adooadoo@163.com
import numpy as np
from sklearn.cluster import k_means
import datetime
import os

class Glove():
    """
    Class for training, using and evaluating glove described in https://code.google.com/p/word2vec/

    The model has three methods:
    1.consine_distance: Calculating the two different word vectors' consine distance
    2.MostSimilarWord: Finding the topN closest words of the given word
    3.clustering: Using sklearn's kmeans to clustering

    """
    def __init__(self, fUrl):
        """
        load model(no-binary model)
        """
        with open(fUrl) as f:
            self.word_dic = {line.split()[0]:np.asarray(line.split()[1:], dtype='float') for line in f}

    def consine_distance(self, word1, word2):
        return np.dot(self.word_dic[word1],self.word_dic[word2])/(np.linalg.norm(self.word_dic[word1])*np.linalg.norm(self.word_dic[word2]))

    def MostSimilarWord(self, word,TopN = 30):
        #print self.word_dic['china']
        return sorted({word2:self.consine_distance(word, word2) for word2 in self.word_dic.keys()}.items(), lambda x, y: cmp(x[1], y[1]), reverse= True) [1:TopN+1]

    def clustering(self, cluster_size):
        X = np.array(list(self.word_dic.itervalues()))
        return k_means(X, n_clusters= cluster_size, init= "k-means++")

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    model = Glove("vectors.txt") #load model
    #print model.MostSimilarWord('china')
    
    cluster_size = 100 #set the cluster's size
    cluster_center, result, inertia = model.clustering(cluster_size)
    keys = model.word_dic.keys() # get all the words

    #write the result into a folder
    resultUrl = 'result'
    os.mkdir(resultUrl)
    f_list = [open(resultUrl+'/'+str(i)+'.txt','w') for i in xrange(cluster_size)]
    [f_list[result_num].write(keys[i]+'\n') for (i, result_num) in enumerate(result)]
    [f_list[i].close() for i in xrange(cluster_size)]#close all the file
    
    r = dict(zip(keys, result))
    print r['china']
    print r['father']
    endtime = datetime.datetime.now()
    print 'Time:', (endtime - starttime).seconds,'s'
    

