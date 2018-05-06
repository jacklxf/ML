import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import*
from nltk.corpus import PlaintextCorpusReader
import re

rating5=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification5','.*')

rating5_words=[]
fids=rating5.fileids()
for fid in fids:
    doc_raw=rating5.raw(fid)
    rating5_words+=nltk.word_tokenize(doc_raw)



rating5_words=[w.lower() for w in rating5_words]
rating5_words=[w for w in rating5_words if re.search ('^[a-z]+$', w)]


stop_list=stopwords.words('english')
rating5_words=[w for w in rating5_words if w not in stop_list]

stemmer=PorterStemmer()
rating5_words=[stemmer.stem(w) for w in rating5_words]

fdist=nltk.FreqDist(rating5_words)
print(fdist.most_common(10))