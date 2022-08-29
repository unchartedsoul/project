
import pandas as pd
import tweepy
import tweepy as OAuthHandler
from textblob import TextBlob
from wordcloud import WordCloud
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")



class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'xxxxxxxxxxxxxxxx'
        consumer_secret = 'xxxxxxxxxxxxxxxxxx'
        access_token = 'XXXXXXXXXXX'
        access_token_secret = 'XXXXXXXXXXXXXX'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet)  # REMOVES @ mentions
        tweet = re.sub(r'#', '', tweet)  # REMOVES # mentions
        tweet = re.sub(r'RT[\s]+', '', tweet)  # REMOVES RT
        tweet = re.sub(r'https?:\/\/\S+', '', tweet)  # REMOVES hyper link
        return  tweet
        # return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])
        #                        | (\w+:\ / \ / \S+)
        # ", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TwitterServerError as e:
            # print error (if any)
            print("Error : " + str(e))


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query='Donald Trump', count=200)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % \
        ".format(100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])


if __name__ == "__main__":
    # calling main function
    main()
# print(data_clean.head())


# clean the text

# creating a function to clear tweets
# def cleantxt(text):
#     text = re.sub(r'@[A-Za-z0-9]+', '', text)  # REMOVES @ mentions
#     text = re.sub(r'#', '', text)  # REMOVES # mentions
#     text = re.sub(r'RT[\s]+', '', text)  # REMOVES RT
#     text = re.sub(r'https?:\/\/\S+', '', text)  # REMOVES hyper link
#
#     return text


# clean the txt
# data_clean = data_clean["tweets"].apply(cleantxt)



# print the clean data
# print(def_clean)


# creating a function to get the subjectivity

# Create a function to get the subjectivity
# def getSubjectivity(text):
#     return TextBlob(text).sentiment.subjectivity
#
#
# # Create a function to get the polarity
# def getPolarity(text):
#     return TextBlob(text).sentiment.polarity
#
#
# # Create two new columns
# data_clean['Subjectivity']= data_clean['tweets'].apply(getSubjectivity)
# data_clean['Polarity'] = data_clean["tweets"].apply(getPolarity)
#
# # Show the new dataframe with the new columns
#
# print(data_clean)