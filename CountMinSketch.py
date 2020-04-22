import random
import requests
from random_word import RandomWords
import tweepy
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class CountMinSketch(object):
    def __init__(self, w, d, p):
        self.w = w
        self.d = d
        self.p = p
        self.C = [[0] * self.w for _ in range(self.d)]
        self.a = [random.randint(1, self.p) for _ in range(self.d)]
        self.b = [random.randint(1, self.p) for _ in range(self.d)]
        self.N = 0

    def hash(self, j, i):
        return (self.a[j] * i + self.b[j] % self.p) % self.w

    def update(self, i, c):
        self.N += c
        for j in range(self.d):
            self.C[j][self.hash(j, i)] += c

    def get(self, i):
        e = self.p + 1
        for j in range(self.d):
            e = min(e, self.C[j][self.hash(j, i)])
        return e


if __name__ == '__main__':

    r = RandomWords()
    test = r.get_random_words(hasDictionaryDef="true", maxLength=6)
    analyser = SentimentIntensityAnalyzer()

    word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"

    response = requests.get(word_site)
    WORDS = response.content.splitlines(0)

    consumer_key = "ew0pmbxpjcfgMTSZcywA0Fgb7"
    consumer_secret = "fO0t6AmR2RvOoAV6aSnVzheDyzCDZz2GJmSWCDsIfjQUXk45fD"
    access_token = "1251440497257672705-datdho4HgxFZoj4AkA8c9cmi0skf8b"
    access_token_secret = "Gw9RnSjfeMzc4P415gbv494VO33fIPU5uGMCXg8qINLl1"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)


    for i in WORDS:
        text_query = str(i)[1:]
        count = 100
        try:
            # Pulling individual tweets from query
            for tweet in api.search(q=text_query, count=count):
                # Adding to list that contains all tweets
                score = analyser.polarity_scores(tweet.text)['compound']
                if (score > 0 or score < 0):
                    print(score)
        except BaseException as e:
            print('failed on_status,', str(e))
            time.sleep(3)


    for data in test:
        text_query = data
        count = 100
        try:
            # Pulling individual tweets from query
            for tweet in api.search(q=text_query, count=count):
                # Adding to list that contains all tweets
                score = analyser.polarity_scores(tweet.text)['compound']
                if (score > 0 or score < 0):
                    print(score)
        except BaseException as e:
            print('failed on_status,', str(e))
            time.sleep(3)









