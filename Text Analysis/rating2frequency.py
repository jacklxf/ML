import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import*
from nltk.corpus import PlaintextCorpusReader
import re

rating2=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification2','.*')

rating2_words=[]
fids=rating2.fileids()
for fid in fids:
    doc_raw=rating2.raw(fid)
    rating2_words+=nltk.word_tokenize(doc_raw)



rating2_words=[w.lower() for w in rating2_words]
rating2_words=[w for w in rating2_words if re.search ('^[a-z]+$', w)]


stop_list=stopwords.words('english')
rating2_words=[w for w in rating2_words if w not in stop_list]

stemmer=PorterStemmer()
rating2_words=[stemmer.stem(w) for w in rating2_words]

fdist=nltk.FreqDist(rating2_words)
print(fdist.most_common(10))