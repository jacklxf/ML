import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import*
from nltk.corpus import PlaintextCorpusReader
import re
import gensim

cluster1=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\cluster1','.*')
cluster2=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\cluster2','.*')
cluster33=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\cluster3','.*')

cluster1_words=[]
fids=cluster1.fileids()
for fid in fids:
    doc_raw=cluster1.raw(fid)
    cluster1_words+=nltk.word_tokenize(doc_raw)

cluster2_words=[]
fids=cluster2.fileids()
for fid in fids:
    doc_raw=cluster2.raw(fid)
    cluster2_words+=nltk.word_tokenize(doc_raw)

cluster3_words=[]
fids=cluster3.fileids()
for fid in fids:
    doc_raw=cluster3.raw(fid)
    cluster3_words+=nltk.word_tokenize(doc_raw)

cluster1_words=[w.lower() for w in cluster1_words]
cluster1_words=[w for w in cluster1_words if re.search ('^[a-z]+$', w)]
stop_list=stopwords.words('english')
cluster1_words=[w for w in cluster1_words if w not in stop_list]
stemmer=PorterStemmer()
cluster1_words=[stemmer.stem(w) for w in cluster1_words]

cluster2_words=[w.lower() for w in cluster2_words]
cluster2_words=[w for w in cluster2_words if re.search ('^[a-z]+$', w)]
stop_list=stopwords.words('english')
cluster2_words=[w for w in cluster2_words if w not in stop_list]
stemmer=PorterStemmer()
cluster2_words=[stemmer.stem(w) for w in cluster2_words]

cluster3_words=[w.lower() for w in cluster3_words]
cluster3_words=[w for w in cluster3_words if re.search ('^[a-z]+$', w)]
stop_list=stopwords.words('english')
cluster3_words=[w for w in cluster3_words if w not in stop_list]
stemmer=PorterStemmer()
cluster3_words=[stemmer.stem(w) for w in cluster3_words]


fdist=nltk.FreqDist(cluster1_words)
print(fdist.most_common(10))
fdist=nltk.FreqDist(cluster2_words)
print(fdist.most_common(10))
fdist=nltk.FreqDist(cluster3_words)
print(fdist.most_common(10))




