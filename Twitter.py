import tweepy,codecs

Consumer_Key="NgFBmwrYkSTMw3TsNxEj5GO4w"
Consumer_Secret="2rrFsWt8UmQoZgxnIFimIsAP44XCVs2cKIeI3Zt7sdZOmXkjr5"
Access_Token="608860877-SvmmykP5RY9YfDHS9i2kWgH7hS7NM17gkj50GQwW"
Access_Secret="O5ycdf4QspwSSxVQCPEvSy8gJGi2fYp9psSs3VsT0rxJV"

auth=tweepy.OAuthHandler(Consumer_Key,Consumer_Secret)
auth.set_access_token(Access_Token,Access_Secret)
api=tweepy.API(auth)

results=api.search(q="sg girl",lang="en",result_type="recent",count=1000)
file=codecs.open("mytweets.txt","w","utf-8")
for result in results:
    file.write(result.text)
    file.write("\n")
file.close()


from aylienapiclient import textapi
client=textapi.Client("9bb7614a","fadb3b451d0aad037203cd232c47aa9c")
sentiment=client.Sentiment({'text':'enter some of your own text here'})
print(sentiment)


from aylienapiclient import textapi
import csv, io

client=textapi.Client("9bb7614a","fadb3b451d0aad037203cd232c47aa9c")

with io.open('MyTweets.csv','w',encoding='utf8',newline='') as csvfile:
    csv_writer=csv.writer(csvfile)
    csv_writer.writerow(['Tweet','Sentiment'])
    with io.open('mytweets.txt','r',encoding='utf8') as f:
        for tweet in f.readlines():
            tweet=tweet.strip()
            
            if len(tweet) == 0:
                print('skipped')
                continue
            
            print(tweet)
            
            sentiment=client.Sentiment({'text':tweet})
            csv_writer.writerow([sentiment['text'],sentiment['polarity']])
            
            
            