# -*- coding: utf-8 -*-

import tweepy
import datetime

_profile=True

QUERY ='"dagsins" -RT lang:is exclude:retweets'

USERNAME = ''

RESULTS_PER_PAGE = '100'
LANGUAGE = 'is'
NUM_PAGES = 1

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = '-'
ACCESS_SECRET = ''

def retweeter():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    retweets = api.retweeted_by_me()

    if retweets:
        created_after = retweets[0].retweeted_status.created_at
    else:
        created_after = datetime.datetime(year=2000, month=1, day=1)

    tweets = api.search(QUERY)
    tweets.reverse()
    for tweet in tweets:
        if not tweet.to_user_id:
            if tweet.created_at > created_after and tweet.from_user != USERNAME:
                api.retweet(tweet.id)
#retweeter()
#import cloud
#cloud.cron.register(retweeter, 'dagsins_retweeter', '*/3 * * * *',_type = 's1')
