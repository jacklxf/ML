import preprocess2
import gensim
sg_corpus = preprocess2.load_corpus('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification_positive')
sg_docs = preprocess2.corpus2docs(sg_corpus)

import gensim
sg_dictionary = gensim.corpora.Dictionary(sg_docs)
sg_vecs = preprocess2.docs2vecs(sg_docs, sg_dictionary)

sg_lda = gensim.models.ldamodel.LdaModel(corpus=sg_vecs, id2word=sg_dictionary, num_topics=5)
topics = sg_lda.show_topics(5,5)
print(topics[0])
print(topics[1])
print(topics[2])
print(topics[3])
print(topics[4])


sg_corpus = preprocess2.load_corpus('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\classification_negative')
sg_docs = preprocess2.corpus2docs(sg_corpus)

sg_dictionary = gensim.corpora.Dictionary(sg_docs)
sg_vecs = preprocess2.docs2vecs(sg_docs, sg_dictionary)

sg_lda = gensim.models.ldamodel.LdaModel(corpus=sg_vecs, id2word=sg_dictionary, num_topics=5)
topics = sg_lda.show_topics(5,5)
print(topics[0])
print(topics[1])
print(topics[2])
print(topics[3])
print(topics[4])