import tweepy

Consumer_Key="NgFBmwrYkSTMw3TsNxEj5GO4w"
Consumer_Secret="2rrFsWt8UmQoZgxnIFimIsAP44XCVs2cKIeI3Zt7sdZOmXkjr5"
Access_Token="608860877-SvmmykP5RY9YfDHS9i2kWgH7hS7NM17gkj50GQwW"
Access_Secret="O5ycdf4QspwSSxVQCPEvSy8gJGi2fYp9psSs3VsT0rxJV"

auth=tweepy.OAuthHandler(Consumer_Key,Consumer_Secret)
auth.set_access_token(Access_Token,Access_Secret)
api=tweepy.API(auth)
"""
#时间线

public_tweets=api.home_timeline(1000)
for tweet in public_tweets:
    print(tweet.text)

#指定id
id='cctv5five'
content=[]
results=api.user_timeline(id,count=1000,lang='en')
for tweet in results:
    content.append(tweet.text)
    
"""
#关键字查找
query="investment"
language="en"
words=api.search(q=query,lang=language,count=1000)
content=[]
for tweet in words:
    content.append(tweet.text)


import numpy as np
import pandas as pd
import nltk
from nltk import word_tokenize
import re
from nltk.corpus import stopwords
stop=stopwords.words('english')

from nltk.stem.porter import*
stemmer=PorterStemmer()

words1=[word_tokenize(i) for i in content]
words2=[[i.lower() for i in doc] for doc in words1]
words3=[[i for i in doc if re.search('^[a-z]+$',i)] for doc in words2]
words4=[[i for i in doc if i not in stop] for doc in words3]
words5=[[stemmer.stem(i) for i in doc] for doc in words4]

text=[]
for i in range(len(words5)):
    for j in words5[i]:
        text.append(j)


from sklearn.feature_extraction.text import CountVectorizer
vec=CountVectorizer()
vec.fit(text)
vec.vocabulary_
vec.vocabulary_.get(u'algorithm')
vec.get_feature_names()
vec.build_analyzer()
vec.build_tokenizer()
vec.tokenizer()






