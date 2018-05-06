import nltk
import gensim
import sys

stop_list = nltk.corpus.stopwords.words('english')
stemmer = nltk.stem.porter.PorterStemmer()

# Open the training data file.
f = open(sys.argv[1], 'r')

# Store the sequence of sentence labels in the following list.
labels = []

# Store the sentences in the following list.
corpus = []

for line in f:
    # For each line of the input file, extract the label and the text.
    (label, tab, text) = line.partition('\t')
    
    # Store the label into the list of labels.
    labels.append(label)
    
    # Tokenize the text.
    sent = nltk.word_tokenize(text)
        
    # Optional!
    # sent2 = [w for w in sent if w not in stop_list]
    
    # Optional!
    # sent3 = [stemmer.stem(w) for w in sent2]
    
    # Store the sentence into the corpus.
    corpus.append(sent)

f.close()

print('Finished reading sentences from the training data file.')

# Create a dictionary from the corpus.
dictionary = gensim.corpora.Dictionary(corpus)

# Store the labeled training data in the following list.
labeled_training_data = []
    
# Going through the two lists in parallel to create the labeled data set.
for (l, s) in zip(labels, corpus):

    # Convert the original sentence into a vector.
    vector = dictionary.doc2bow(s)
    
    # Create a dict object to store the document vector (in order to use NLTK's classifier later)
    sent_as_dict = {id:1 for (id, tf) in vector}
    
    # Add the labeled sentence to the labeled data set.
    labeled_training_data.append((sent_as_dict, l))
    
print('Finished preparing the training data.')

# Training a classifier.
# Choose one of the following two classification algorithms to train a classifier.
classifier = nltk.NaiveBayesClassifier.train(labeled_training_data)
# classifier = nltk.MaxentClassifier.train(labeled_training_data)

print('Finished training the classifier.')

# Testing the accuracy of the classifier on a separate data set.

# Open the test data file.
f = open(sys.argv[2], 'r')

labels = []
corpus = []

for line in f:
    (label, tab, text) = line.partition('\t')
    labels.append(label)
    sent = nltk.word_tokenize(text)
        
    # Optional!
    # sent2 = [w for w in sent if w not in stop_list]
    
    # Optional!
    # sent3 = [stemmer.stem(w) for w in sent2]
    
    corpus.append(sent)
f.close()

print('Finished reading sentences from the test data file.')

# Store the labeled test data in the following list.
labeled_test_data = []
    
# Going through the two lists in parallel to create the labeled data set.
for (l, s) in zip(labels, corpus):

    # Convert the original sentence into a vector.
    vector = dictionary.doc2bow(s)
    
    # Create a dict object to store the document vector (in order to use NLTK's classifier later)
    sent_as_dict = {id:1 for (id, tf) in vector}
    
    # Add the labeled sentence to the labeled data set.
    labeled_test_data.append((sent_as_dict, l))
    
print('Finished preparing the test data.')

# Test the accuracy.
print("Accuracy on test data: ", nltk.classify.accuracy(classifier, labeled_test_data))