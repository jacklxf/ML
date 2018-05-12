#try demo 1
import demo
y = demo.square(4)
print(y)

#try demo 2
from demo import square
y = square(4)
print(y)

#try test
import postgresETL
print(postgresETL.repeat('hello', 3))

#try preprocess and perform clustering with K-means
import preprocess
import k_means
from preprocess import *
import gensim
corpus = load_corpus('SGNewsForClustering')
docs = corpus2docs(corpus)
dictionary = gensim.corpora.Dictionary(docs)
vecs = docs2vecs(docs,dictionary)
print(dictionary)
clusters = k_means.k_means(vecs, 2217, 2)   #use K-means to cluster all the documents into two clusters
cluster1 = clusters[0] 
print(cluster1) # the document indexes in the first cluster
fids=corpus.fileids()
print([fids[d] for d in cluster1]) # the original document names in the first cluster

#######use NLTKs FreqDist class to check the most frequent words of cluster1########
import nltk
from nltk.corpus import PlaintextCorpusReader
import os
import re
from nltk.corpus import stopwords

#read all the documents in cluster1, and then save them into a new file named test.txt
fold_name = 'SGNewsForClustering' + os.sep
fout = open('test.txt', 'w')
for d in cluster1:
    fin = open(fold_name+fids[d], 'r')
    for line in fin.readlines():
        fout.write(line)
fout.close()
#After this, you will see a test.txt file

#Then, use the knowledge we learn in previous 4 labs to find the most frequent words
corpus = PlaintextCorpusReader('', '.*')
test = corpus.words('test.txt')
test_lower = [w.lower() for w in test] # changing everything to lowercase
test_words_only = [w for w in test_lower if re.search('^[a-z]+$',w)] #removing punctuation marks
stop_list = stopwords.words('english') 
test_stopremoved = [w for w in test_words_only if w not in stop_list] #Stop Word Removal
fdist = nltk.FreqDist(test_stopremoved) 
print(fdist.most_common(10)) #use nltk to  find the most common 10 words in cluster1





