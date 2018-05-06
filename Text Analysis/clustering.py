from preprocess2 import*
import k_means

corpus=load_corpus('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\Reviews')
docs=corpus2docs(corpus)
dictionary=gensim.corpora.Dictionary(docs)
vecs=docs2vecs(docs,dictionary)
#print(dictionary)

clusters=k_means.k_means(vecs,38644,3)
#print(clusters)

cluster1=clusters[0]
cluster2=clusters[1]
cluster3=clusters[2]

fids=corpus.fileids()
corpus_cluster1=[fids[d] for d in cluster1]
corpus_cluster2=[fids[d] for d in cluster2]
corpus_cluster3=[fids[d] for d in cluster3]

fname = 'cluster1'
fout = open(fname, 'w')
for i in range(len(corpus_cluster1)):
    fout.write(str(corpus_cluster1[i])+ '\n')
fout.close()


import os

fname = 'cluster1'
fin = open(fname, 'r')
cluster1_file_name = []
for line in fin.readlines():
    file_name = line.strip()
    cluster1_file_name.append(file_name)


path = 'C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\Reviews'+os.sep
for file in os.listdir(path):
    if os.path.isfile(os.path.join(path,file))==True:
        if file in cluster1_file_name:
            newname= 'cluster1' + file
            os.rename(os.path.join(path,file),os.path.join(path,newname))