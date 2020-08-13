#based on https://gist.github.com/yanofsky/5436496
#downloads and writes all available tweets from an account into a txt file
#tweets seperated by ß
#!/usr/bin/env python
# encoding: utf-8

import sys
import tweepy #https://github.com/tweepy/tweepy

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

#Twitter account

account = sys.argv[1] 

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200, tweet_mode="extended")
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest, tweet_mode="extended")
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...%s tweets downloaded so far" % (len(alltweets)))

	#get rid of retweets
	alltweets_wo_retweets = [tweet for tweet in alltweets if not hasattr(tweet,'retweeted_status')]

	print("\n\n")
	print("%s tweets downloaded in total" % (len(alltweets)))
	print("%s tweets without retweets" % (len(alltweets_wo_retweets)))

	#write tweets as one string into variable
	outtweets = [tweet.full_text for tweet in alltweets_wo_retweets]

	print("\n\n")
	print(outtweets[0]+  "\n\n")

	CountTweets = len(outtweets)
	firstTweet = alltweets_wo_retweets[CountTweets-1].created_at.strftime("%Y-%m-%d")
	lastTweet = alltweets_wo_retweets[0].created_at.strftime("%Y-%m-%d")

	#write the txt	
	f= open(account + "_" + str(CountTweets) + "_tweets_" + firstTweet + "_" + lastTweet + ".txt","w+")

	for i in range(len(outtweets)):
		f.write(outtweets[i] + "ß")

	f.close()


get_all_tweets(account)
