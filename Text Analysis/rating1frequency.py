import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import*
from nltk.corpus import PlaintextCorpusReader
import re


rating1=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification1','.*')


rating1_words=[]
fids=rating1.fileids()
for fid in fids:
    doc_raw=rating1.raw(fid)
    rating1_words+=nltk.word_tokenize(doc_raw)



rating1_words=[w.lower() for w in rating1_words]
rating1_words=[w for w in rating1_words if re.search ('^[a-z]+$', w)]


stop_list=stopwords.words('english')
rating1_words=[w for w in rating1_words if w not in stop_list]

stemmer=PorterStemmer()
rating1_words=[stemmer.stem(w) for w in rating1_words]

fdist=nltk.FreqDist(rating1_words)
print(fdist.most_common(10))



