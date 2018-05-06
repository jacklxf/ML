import nltk
import re
import gensim
import preprocess2
from nltk.corpus import stopwords
from nltk.stem.porter import*
from gensim import corpora
from nltk.corpus import PlaintextCorpusReader
rating1=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\training\\rating1','.*')
rating2=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\training\\rating2','.*')
rating3=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\training\\rating3','.*')
rating4=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\training\\rating4','.*')
rating5=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\training\\rating5','.*')

rating1_docs=[rating1.words(fid) for fid in rating1.fileids()]
rating2_docs=[rating2.words(fid) for fid in rating2.fileids()]
rating3_docs=[rating3.words(fid) for fid in rating3.fileids()]
rating4_docs=[rating4.words(fid) for fid in rating4.fileids()]
rating5_docs=[rating5.words(fid) for fid in rating5.fileids()]

all_docs=rating1_docs+rating2_docs+rating3_docs+rating4_docs+rating5_docs
#print (all_docs)


all_docs=[[w.lower() for w in doc] for doc in all_docs]
all_docs=[[w for w in doc if re.search ('^[a-z]+$', w)] for doc in all_docs]
stop_list=stopwords.words('english')
all_docs=[[w for w in doc if w not in stop_list] for doc in all_docs]
stemmer=PorterStemmer()
all_docs=[[stemmer.stem(w) for w in doc] for doc in all_docs]
#print (all_docs)

dictionary=corpora.Dictionary(all_docs)
all_tf_vectors=[dictionary.doc2bow(doc) for doc in all_docs]
#print (all_tf_vectors)

all_data_as_dict=[{id:1 for (id,tf_value) in vec} for vec in all_tf_vectors]
rating1_class=[(d,'rating1') for d in all_data_as_dict[0:9]]
rating2_class=[(d,'rating2') for d in all_data_as_dict[10:19]]
rating3_class=[(d,'rating3') for d in all_data_as_dict[20:29]]
rating4_class=[(d,'rating4') for d in all_data_as_dict[30:39]]
rating5_class=[(d,'rating5') for d in all_data_as_dict[40:49]]
all_labeled_data=rating1_class+rating2_class+rating3_class+rating4_class+rating5_class
#print(all_labeled_data)

classifier=nltk.NaiveBayesClassifier.train(all_labeled_data)

mp3_corpus=PlaintextCorpusReader('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\Reviews','.*')
fids=mp3_corpus.fileids()
#print (fids)

mp3_docs=preprocess2.corpus2docs(mp3_corpus)
mp3_docs=[[w for w in doc if re.search('^[a-z]+$',w)] for doc in mp3_docs]
mp3_docs=[[stemmer.stem(w) for w in doc] for doc in mp3_docs]
#print (mp3_docs)

mp3_dictionary=gensim.corpora.Dictionary(mp3_docs)
#print (mp3_dictionary)
test_vectors=[mp3_dictionary.doc2bow(doc) for doc in mp3_docs]
#print (test_vectors)

test_data_as_dict=[{id:1 for (id,tf_value) in vec} for vec in test_vectors]
#print (test_data_as_dict)
print(classifier.classify(test_data_as_dict[0]))
