import nltk
import re
import gensim
import preprocess2
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.stem.porter import*
from gensim import corpora
from nltk.corpus import PlaintextCorpusReader

rating1=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification1','.*')
rating2=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification2','.*')
rating3=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification3','.*')
rating4=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification4','.*')
rating5=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification5','.*')

rating1_words=[]
rating2_words=[]
rating3_words=[]
rating4_words=[]
rating5_words=[]

fids=rating1.fileids()
for fid in fids:
    doc_raw=rating1.raw(fid)
    rating1_words+=nltk.word_tokenize(doc_raw)

fids=rating2.fileids()
for fid in fids:
    doc_raw=rating2.raw(fid)
    rating2_words+=nltk.word_tokenize(doc_raw)

fids=rating3.fileids()
for fid in fids:
    doc_raw=rating3.raw(fid)
    rating3_words+=nltk.word_tokenize(doc_raw)

fids=rating4.fileids()
for fid in fids:
    doc_raw=rating4.raw(fid)
    rating4_words+=nltk.word_tokenize(doc_raw)

fids=rating5.fileids()
for fid in fids:
    doc_raw=rating5.raw(fid)
    rating5_words+=nltk.word_tokenize(doc_raw)

#print(rating1_words)
#print(rating2_words)
#print(rating3_words)
#print(rating4_words)
#print(rating5_words)


all_words=rating1_words+rating2_words+rating3_words+rating4_words+rating5_words
#print (all_docs)

all_words=[[w.lower() for w in doc] for doc in all_words]
all_words=[[w for w in doc if re.search ('^[a-z]+$', w)] for doc in all_words]
stop_list=stopwords.words('english')
all_words=[[w for w in doc if w not in stop_list] for doc in all_words]
stemmer=PorterStemmer()
all_words=[[stemmer.stem(w) for w in doc] for doc in all_words]
print (all_words)

'''
fdist=nltk.FreqDist(all_docs[0])
print(fdist.most_common(10))

fdist=nltk.FreqDist(all_docs[1])
print(fdist.most_common(10))

fdist=nltk.FreqDist(all_docs[2])
print(fdist.most_common(10))

fdist=nltk.FreqDist(all_docs[3])
print(fdist.most_common(10))

fdist=nltk.FreqDist(all_docs[4])
print(fdist.most_common(10))
'''