import numpy as np 
import time 
import matplotlib.pyplot as plt
import tweepy

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator

from count_min_sketch import CountMinSketch
from count_sketch_median import CountMedianSketch

consumer_key = "ew0pmbxpjcfgMTSZcywA0Fgb7"
consumer_secret = "fO0t6AmR2RvOoAV6aSnVzheDyzCDZz2GJmSWCDsIfjQUXk45fD"
access_token = "1251440497257672705-datdho4HgxFZoj4AkA8c9cmi0skf8b"
access_token_secret = "Gw9RnSjfeMzc4P415gbv494VO33fIPU5uGMCXg8qINLl1"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

class MyStreamListener(tweepy.StreamListener):
        
    translator = Translator()
    analyser = SentimentIntensityAnalyzer()

    def set_real_counter(self, shape):
        self.counts = np.zeros(shape)

    def get_sentiment(self, text):
        score = self.analyser.polarity_scores(text)
        return score['compound']

    def on_status(self, status):
        if status.lang != 'en': return
        text = status.text.lower()
        print(text) 

        try:
            likes = status.retweeted_status.favorite_count
        except:
            likes = status.favorite_count
        
        sentiment = self.get_sentiment(text)
        # try:
        #     sentiment = self.get_sentiment(text)
        # except:
        #     return

        for i in range(len(topics)):
            topic = topics[i]
            subtopics = topic.split(' ')
            for sub in subtopics:
                if sub in text:
                    val = np.array([1, sentiment, likes])
                    self.counts[i] += val
                    csketch.insert(i, val)
                    break

        all_val = csketch.query_all()

        a[0].set_title('counts')
        a[1].set_title('sentiments')
        a[2].set_title('likes')
        arange_ind = np.arange(all_val.shape[0])

        for i in range(len(a)):
            a[i].grid()
            a[i].plot(arange_ind, all_val[:, i], 'r')
            a[i].plot(arange_ind, self.counts[:, i], 'b--')
            a[i].set_xticks(arange_ind)

        a[2].set_xticklabels(topics, rotation=90)
        
        plt.pause(1e-17)
        
        for sub_a in a: sub_a.cla()
        
        print(np.sum(self.counts, axis = 0))
        time.sleep(0.01)

if __name__ == '__main__':
    # topics = ['bloomberg', 'bennet', 'bernie', 'booker', 'bullock', 'buttigieg', 'castro', 'blasio', 'delaney',
    #          'gabbard', 'gillibrand', 'harris', 'hickenlooper', 'inslee', 'klobuchar', 'messam', 
    #          'moulton', 'ojeda', 'rourke', 'deval', 'ryan', 'sestak', 'steyer', 'swalwell', 
    #          'warren', 'williamson', 'yanggang']
    
    # topics = ['stacey abrams', 'michelle obama', 'tammy baldwin', 'cory booker', 'sherrod brown', 'pete buttigieg', 'bob casey', 'julian castro', 'catherine cortez mastro', 'val demings', 'tammy duckworth',
    # 'kamala harris', 'maggie hassan', 'jahana hayes', 'doug jones', 'laura kelly', 'amy klobuchar', 'keisha lance bottoms', 'brenda lawrence', 'michelle lunjam grisham', 'gavin newsom', 'susan rice',
    # 'terri sewell', 'jeanne shaheen', 'elizabeth warren', 'gretchen whitmer', 'andrew yang', 'sally yates'
    # ]
    
    topics = ['kim jong un', 'kim yo jong', 'nike', 'lockdown', 'donald trump', 'corona virus', 'netflix', 'zoom', 'apple iphone', 'tiktok', 'youtube', 'facebook', 'instagram']

    ch = 3
    myStreamListener = MyStreamListener()
    myStreamListener.set_real_counter((len(topics), ch))
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

    # csketch = CountMedianSketch(len(topics), 3)
    csketch = CountMinSketch(len(topics), ch)

    plt.show()
    fig, a =  plt.subplots(ch, 1)
    print('node starting to track')
    while True:
        myStream.filter(track=topics)
        # try:
        #     myStream.filter(track=topics)
        # except:
        #     continue
    plt.show()