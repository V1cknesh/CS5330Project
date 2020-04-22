import tweepy
import numpy as np 
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import time 
import matplotlib.pyplot as plt

from count_min_sketch import CountMinSketch
from count_sketch_median import MedianCountSketch

consumer_key = "ew0pmbxpjcfgMTSZcywA0Fgb7"
consumer_secret = "fO0t6AmR2RvOoAV6aSnVzheDyzCDZz2GJmSWCDsIfjQUXk45fD"
access_token = "1251440497257672705-datdho4HgxFZoj4AkA8c9cmi0skf8b"
access_token_secret = "Gw9RnSjfeMzc4P415gbv494VO33fIPU5uGMCXg8qINLl1"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

translator = Translator()
analyser = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyser.polarity_scores(text)
    return score['compound']

class MyStreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        if status.lang != 'en': return
        text = status.text.lower()
        print(text)        

        try:
            likes = status.retweeted_status.favorite_count
        except:
            likes = status.favorite_count
        

        try:
            sentiment = get_sentiment(text)
        except:
            return

        for i in range(len(topics)):
            topic = topics[i]
            if topic in text:
                #send packet to counter
                msg = [topic, sentiment]
                counts[0, i] += 1
                counts[1, i] += sentiment
                counts[2, i] += likes

                csketch_counts.insert(i, 1)
                csketch_sentiments.insert(i, sentiment)
                csketch_likes.insert(i, likes)

        a[0].set_title('counts')
        a[1].set_title('sentiments')
        a[2].set_title('likes')

        a[0].plot(np.arange(counts.shape[1]), counts[0], 'b')
        a[1].plot(np.arange(counts.shape[1]), counts[1], 'b')
        a[2].plot(np.arange(counts.shape[1]), counts[2], 'b')

        a[0].plot(np.arange(counts.shape[1]), csketch_counts.get_counter(), 'r')
        a[1].plot(np.arange(counts.shape[1]), csketch_sentiments.get_counter(), 'r')
        a[2].plot(np.arange(counts.shape[1]), csketch_likes.get_counter(), 'r')


        a[0].set_xticks(np.arange(counts.shape[1]))
        a[1].set_xticks(np.arange(counts.shape[1]))
        a[2].set_xticks(np.arange(counts.shape[1]))

        a[2].set_xticklabels(topics, rotation=90)
        
        plt.pause(1e-17)
        
        a[0].cla()
        a[1].cla()
        a[2].cla()
        
        time.sleep(0.1)

topics = ['trump', 'biden', 'bloomberg', 'bennet', 'booker', 'bullock', 'buttigieg', 'castro', 'blasio', 'delaney',
         'gabbard', 'gillibrand', 'mike gravel', 'harris', 'hickenlooper', 'inslee', 'klobuchar', 'messam', 
         'moulton', 'ojeda', 'rourke', 'deval', 'ryan', 'bernie', 'sestak', 'steyer', 'swalwell', 
         'warren', 'williamson', 'yang']

counts = np.zeros((3, len(topics)))
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

csketch_counts = MedianCountSketch(len(topics), 8, 0.1)
csketch_sentiments = MedianCountSketch(len(topics), 8, 0.1)
csketch_likes = MedianCountSketch(len(topics), 8, 0.1)

# csketch_counts = CountMinSketch(len(topics), 0.1)
# csketch_sentiments = CountMinSketch(len(topics), 0.1)
# csketch_likes = CountMinSketch(len(topics), 0.1)

plt.show()
fig, a =  plt.subplots(3, 1)

print('node starting to track')


myStream.filter(track=topics)
# while True:
#     try:
#         myStream.filter(track=topics)
#     except:
#         continue

plt.show()