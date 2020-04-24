Analysis of Count Sketch Algorithms by passing in an input stream of data.


Setting up the stream API converting tweets to sentiments.

1. Register for a twitter developer account.
2. Create your application and obtain the consumer_key, consumer_secret, access_token, access_token_secret
3. pip install tweepy
4. Use the python tweepy API to read tweets.
4. We have generated a list of random words and pulled tweets from twitter.
5. We will be analysing the general sentiment of tweets.
6. pip install vaderSentiment
7. Vader will convert the tweets to sentiment scores (between -1 and 1).
8. CreateSentiment.py will create the sentiment file by converting tweets to its sentiment scores.
9. It is possible to replace the twitter stream with any other stream of data.


Running the CountMinSketch algorithm

1. CountMinSketch.py will read the data from sentiment.txt and pass it into the algorithm.


Performance Analysis using memory profiler

1. pip install -U memory_profiler
2. Add the @profile annotation on each function you wish to analyse the memory consumption.

3. python -m memory_profiler CountMinSketch.py

4. mprof run CountMinSketch.py
5. mprof plot


