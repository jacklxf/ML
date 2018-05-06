import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import*
from nltk.corpus import PlaintextCorpusReader
import re

rating3=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification3','.*')

rating3_words=[]
fids=rating3.fileids()
for fid in fids:
    doc_raw=rating3.raw(fid)
    rating3_words+=nltk.word_tokenize(doc_raw)



rating3_words=[w.lower() for w in rating3_words]
rating3_words=[w for w in rating3_words if re.search ('^[a-z]+$', w)]


stop_list=stopwords.words('english')
rating3_words=[w for w in rating3_words if w not in stop_list]

stemmer=PorterStemmer()
rating3_words=[stemmer.stem(w) for w in rating3_words]

fdist=nltk.FreqDist(rating3_words)
print(fdist.most_common(10))