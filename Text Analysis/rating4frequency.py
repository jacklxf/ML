import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import*
from nltk.corpus import PlaintextCorpusReader
import re

rating4=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification4','.*')

rating4_words=[]
fids=rating4.fileids()
for fid in fids:
    doc_raw=rating4.raw(fid)
    rating4_words+=nltk.word_tokenize(doc_raw)



rating4_words=[w.lower() for w in rating4_words]
rating4_words=[w for w in rating4_words if re.search ('^[a-z]+$', w)]


stop_list=stopwords.words('english')
rating4_words=[w for w in rating4_words if w not in stop_list]

stemmer=PorterStemmer()
rating4_words=[stemmer.stem(w) for w in rating4_words]

fdist=nltk.FreqDist(rating4_words)
print(fdist.most_common(10))