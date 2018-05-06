import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import*
from nltk.corpus import PlaintextCorpusReader
import re
import gensim

rating1=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification1','.*')
rating2=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification2','.*')
rating3=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification3','.*')
rating4=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification4','.*')
rating5=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification5','.*')

rating1_words=[]
fids=rating1.fileids()
for fid in fids:
    doc_raw=rating1.raw(fid)
    rating1_words+=nltk.word_tokenize(doc_raw)

rating2_words=[]
fids=rating2.fileids()
for fid in fids:
    doc_raw=rating2.raw(fid)
    rating2_words+=nltk.word_tokenize(doc_raw)

rating3_words=[]
fids=rating3.fileids()
for fid in fids:
    doc_raw=rating3.raw(fid)
    rating3_words+=nltk.word_tokenize(doc_raw)

rating4_words=[]
fids=rating4.fileids()
for fid in fids:
    doc_raw=rating4.raw(fid)
    rating4_words+=nltk.word_tokenize(doc_raw)

rating5_words=[]
fids=rating5.fileids()
for fid in fids:
    doc_raw=rating5.raw(fid)
    rating5_words+=nltk.word_tokenize(doc_raw)

rating1_words=[w.lower() for w in rating1_words]
rating1_words=[w for w in rating1_words if re.search ('^[a-z]+$', w)]
stop_list=stopwords.words('english')
rating1_words=[w for w in rating1_words if w not in stop_list]
stemmer=PorterStemmer()
rating1_words=[stemmer.stem(w) for w in rating1_words]

rating2_words=[w.lower() for w in rating2_words]
rating2_words=[w for w in rating2_words if re.search ('^[a-z]+$', w)]
stop_list=stopwords.words('english')
rating2_words=[w for w in rating2_words if w not in stop_list]
stemmer=PorterStemmer()
rating2_words=[stemmer.stem(w) for w in rating2_words]

rating3_words=[w.lower() for w in rating3_words]
rating3_words=[w for w in rating3_words if re.search ('^[a-z]+$', w)]
stop_list=stopwords.words('english')
rating3_words=[w for w in rating3_words if w not in stop_list]
stemmer=PorterStemmer()
rating3_words=[stemmer.stem(w) for w in rating3_words]

rating4_words=[w.lower() for w in rating4_words]
rating4_words=[w for w in rating4_words if re.search ('^[a-z]+$', w)]
stop_list=stopwords.words('english')
rating4_words=[w for w in rating4_words if w not in stop_list]
stemmer=PorterStemmer()
rating4_words=[stemmer.stem(w) for w in rating4_words]

rating5_words=[w.lower() for w in rating5_words]
rating5_words=[w for w in rating5_words if re.search ('^[a-z]+$', w)]
stop_list=stopwords.words('english')
rating5_words=[w for w in rating5_words if w not in stop_list]
stemmer=PorterStemmer()
rating5_words=[stemmer.stem(w) for w in rating5_words]


fdist=nltk.FreqDist(rating1_words)
print(fdist.most_common(10))
fdist=nltk.FreqDist(rating2_words)
print(fdist.most_common(10))
fdist=nltk.FreqDist(rating3_words)
print(fdist.most_common(10))
fdist=nltk.FreqDist(rating4_words)
print(fdist.most_common(10))
fdist=nltk.FreqDist(rating5_words)
print(fdist.most_common(10))


'''
all_words=rating1_words+rating2_words+rating3_words+rating4_words+rating5_words

f=open('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\wordcloud.txt','w')
f.write(str(all_words))
f.close()


positive_words=rating4_words+rating5_words
negative_words=rating1_words+rating2_words

f=open('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\positive_words.txt','w')
f.write(str(positive_words))
f.close()

f=open('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\negative_words.txt','w')
f.write(str(negative_words))
f.close()
'''


