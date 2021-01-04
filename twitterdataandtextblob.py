import requests
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from matplotlib import pyplot as plt
import numpy as np
import json


search_words = '#coronavirus'
date_since = "2021-01-01"

class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		consumer_key = ' '
		consumer_secret = ' '
		access_token = ' '
		access_token_secret = ' '

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
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", tweet).split())

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

	def get_tweets(self, query, count = 200):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []
	

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q=search_words, lang="en" , since = date_since, count = count)

			print(type(fetched_tweets))

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving retweetcount of tweet
				parsed_tweet['retweet'] = tweet.retweet_count
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 50:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

def main():
	# creating object of TwitterClient Class
	api = TwitterClient()
	# calling function to get tweets
	tweets = api.get_tweets(query = 'SEARCH', count = 200)

	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	# percentage of positive tweets
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
	# picking negative tweets from tweets
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# percentage of negative tweets
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
	# percentage of neutral tweets
	print("Neutral tweets percentage: {} % \ ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))

	# printing first 5 positive tweets
	print("\n\nPositive tweets:")
	for tweet in ptweets[:20]:
		print(tweet['text'],tweet['retweet'])

	# printing first 5 negative tweets
	print("\n\nNegative tweets:")

	for tweet in ntweets[:20]:
		print(tweet['text'],tweet['retweet'])

	#representing the pie chart
	reaction = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']

	data = [(100*len(ptweets)/len(tweets)),(100*len(ntweets)/len(tweets)),(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))]


	# Creating plot
	fig = plt.figure(figsize=(10, 7))
	plt.pie(data, labels= reaction)

	# show plot
	plt.show()

if __name__ == "__main__":
	# calling main function
	main()
