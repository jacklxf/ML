import nltk
import sys

# Read the positive sentiment lexicon.
pos_dict = {}
f = open('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\positive-words.txt', 'r')
for line in f:
    line = line.strip()
    pos_dict[line] = 1
f.close()

# Read the negative sentiment lexicon.
neg_dict = {}
f = open('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\negative-words.txt', 'r')
for line in f:
    line = line.strip()
    neg_dict[line] = 1
f.close()

# Store the sequence of sentence labels in the following list.
labels = []

# Store the sentences in the following list.
corpus = []

f = open('C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\UICReviewData\\Nikon.txt', 'r')

for line in f:
    # For each line of the input file, extract the label and the text.
    (label, tab, text) = line.partition('\t')
    
    # Store the label into the list of labels.
    labels.append(label)
    
    # Tokenize the text.
    sent = nltk.word_tokenize(text)
    
    # Add the sentence to the corpus
    corpus.append(sent)

f.close()

print('Finished reading sentences from the data file.')

# The following list stores the predicted labels.
predicted_labels = []

for sent in corpus:
    score = 0
    for w in sent:
        # If the word w is inside the positive lexicon, then increase the score by 1.
        if w in pos_dict:
            score = score + 1
        # If the word w is inside the negative lexicon, then decrease the score by 1.
        # elif means "else if"
        elif w in neg_dict:
            score = score - 1
    if score >= 0:
        predicted_labels.append('+')
    else:
        predicted_labels.append('-')

# Compute the accuracy of the predicted labels.
total = len(labels)
correct = 0

for (tl, pl) in zip(labels, predicted_labels):
    if tl == pl:
        correct = correct + 1

accu = correct / total
print("Accuracy: ", accu)