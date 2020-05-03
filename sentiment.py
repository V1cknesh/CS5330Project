import numpy as np 
import time 
import matplotlib.pyplot as plt
import tweepy
import sys

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator

from count_min_sketch import CountMinSketch
from count_sketch_median import CountMedianSketch
from random_word import RandomWords
from benchmarking import get_size

consumer_key = "ew0pmbxpjcfgMTSZcywA0Fgb7"
consumer_secret = "fO0t6AmR2RvOoAV6aSnVzheDyzCDZz2GJmSWCDsIfjQUXk45fD"
access_token = "1251440497257672705-datdho4HgxFZoj4AkA8c9cmi0skf8b"
access_token_secret = "Gw9RnSjfeMzc4P415gbv494VO33fIPU5uGMCXg8qINLl1"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

class MyStreamListener(tweepy.StreamListener):
    time_count = 0
    translator = Translator()
    analyser = SentimentIntensityAnalyzer()

    def set_real_counter(self, shape):
        self.counts = np.zeros(shape)

    def get_sentiment(self, text):
        score = self.analyser.polarity_scores(text)
        return score['compound']

    def on_status(self, status):
        # if status.lang != 'en': return
        text = status.text.lower()
        print(text) 
        outf.write(text)
        outf.write("\n")

        try:
            likes = status.retweeted_status.favorite_count
        except:
            likes = status.favorite_count
        
        sentiment = self.get_sentiment(text)

        for i in range(len(topics)):
            topic = topics[i]
            subtopics = topic.split(' ')
            for sub in subtopics:
                if sub in text:
                    val = np.array([1, sentiment, likes])
                    self.counts[i] += val
                    csketch.insert(i, val)
                    break
        print(np.sum(self.counts, axis = 0)[0])
        if np.sum(self.counts, axis = 0)[0]%50 == 0:
            print('size ', get_size(csketch))


            start = time.time()
            all_val = csketch.query_all()
            end = time.time()
            f.write("query time: " + str(end-start) + "s \n")
            print('query_all time : ', end - start)

            a[0].set_title('counts')
            a[1].set_title('sentiments')
            a[2].set_title('likes')
            arange_ind = np.arange(all_val.shape[0])

            for i in range(len(a)):
                a[i].grid()
                a[i].plot(arange_ind, all_val[:, i], 'r')
                a[i].plot(arange_ind, self.counts[:, i], 'b--')
                a[i].set_xticks(arange_ind)

            a[2].set_xticklabels(topics, rotation=90, fontsize = 10)
            fig.tight_layout()

            if np.sum(self.counts, axis = 0)[0]%1000 == 0:
                plt.savefig('./result_tweets/politicians.png')        
            
            plt.pause(1e-17)
            
            for sub_a in a: sub_a.cla()
            
            for i in range(len(a)):
                f.write("accuracy for " + str(i) + ":"+ str(1-np.sqrt(((self.counts[:, i] - all_val[:,i]) ** 2).mean())/(np.max(all_val[:,i]) - np.min(all_val[:,i]) ))+ "\n")
                f.write("memory Consumption" + str(sys.getsizeof(csketch)) + "\n")
            print(np.sum(self.counts, axis = 0))            
            # time.sleep(0.01)

        print('elapsed time: ', time.time()-track_start)

        # self.time_count = self.time_count+1
        # if self.time_count > 1000:
        #     return False

if __name__ == '__main__':

    # r = RandomWords()
    # topics = r.get_random_words(hasDictionaryDef="true")
    # print(topics)    

    topics = ['kim jong un', 'kim yo jong', 'jacinda ardern', 'boris johnson', 'emmanuel macron', 'giuseppe conte', 'xi jinping', 'vladimir putin', 'angela merkel', 'narendra modi', 'jokowi', 'lee hsien loong', 'muhyiddin yassin', 'najib razak', 'justin trudeau', 
    'donald trump', 'mike pence', 'andrew cuomo', 'joe biden', 'bernie sanders', 'aoc', 'nancy pelosi', 
    'stacey abrams', 'michelle obama', 'tammy baldwin', 'cory booker', 'sherrod brown', 'pete buttigieg', 'bob casey', 'julian castro', 'catherine cortez mastro', 'val demings', 'tammy duckworth',
    'kamala harris', 'maggie hassan', 'jahana hayes', 'doug jones', 'laura kelly', 'amy klobuchar', 'keisha lance bottoms', 'brenda lawrence', 'michelle lunjam grisham', 'gavin newsom', 'susan rice',
    'terri sewell', 'jeanne shaheen', 'elizabeth warren', 'gretchen whitmer', 'andrew yang', 'sally yates']
    
    # topics = ['singapore', 'kuala lumpur', 'hanoi', 'jakarta', 'rome', 'bangkok', 'tokyo', 'delhi', 'seoul', 'beijing', 'hongkong', 'shanghai', 'milan', 'yangon', 
    # 'sydney', 'christchurch', 'manila', 'taipei', 'san francisco', 'los angeles', 'las vegas', 'chicago', 'dallas', 'miami', 'new york', 'toronto', 'vancouver', 'lima',
    # 'london', 'paris', 'belgium', 'berlin', 'rome', 'madrid', 'lisbon', 'stockholm', 'oslo', 'copenhagen', 'helsinki', 'istanbul', 'dubai', 'johannesburg', 'lahore', 'dhaka', 'moscow',
    # 'pyongyang', 'sao paulo', 'cairo', 'mumbai', 'osaka', 'karachi', 'kolkata', 'buenos aires', 'rio janeiro', 'shenzhen', 'bogota', 'chennai', 'melbourne', 'wuhan', 
    # 'nairobi'
    # ]

    # topics.sort()
    print(len(topics))

    ch = 3
    myStreamListener = MyStreamListener()
    myStreamListener.set_real_counter((len(topics), ch))
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

    csketch = CountMedianSketch(len(topics), ch)
    # csketch = CountMinSketch(len(topics), ch)

    outf = open("./tweets.txt", "w+")

    f = open("out.txt", "w")
    # f.write("settings: episilon" + str(epsilon) + "\n")

    plt.show()
    fig, a =  plt.subplots(ch, 1)
    print('node starting to track')
    track_start = time.time()
    while True:
        try:
            myStream.filter(track=topics)   
        except:
            continue
    
    plt.show()
