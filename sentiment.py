import tweepy
import numpy as np 
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time 
from googletrans import Translator

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
    trans = translator.translate(text).text 
    score = analyser.polarity_scores(trans)
    return score['compound']

class MyStreamListener(tweepy.StreamListener):
    sentiment_score = 0
    
    def on_status(self, status):
        try:
            val = get_sentiment(status.text)
            self.sentiment_score +=  val
        except:
            return

        print(str(self.sentiment_score)+' '+ status.text , end='\r', flush=True)
        # print(self.sentiment_score, sep=' ', end='', flush=True)
        
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['trump'])