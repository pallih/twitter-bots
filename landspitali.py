# -*- coding: utf-8 -*-
import requests
import lxml.html
import time
import datetime
import tweepy
import random
import string

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_SECRET = ''

chars = string.letters + string.digits
randomstring=  ''.join([random.choice(chars) for i in xrange(4)]) # create a random string for url appending to avoid cache

def landspitali_tweet():
	url = 'http://landspitali.is?x=' + randomstring
	html = requests.get(url).text
	root = lxml.html.fromstring(html)
	space = ' '
	strings = root.xpath('//div[@class="activityNumbers activityNumbersNew"]')
	for s in strings:
		record = {}
   	 	messages = []
   	 	for d in s[1:]:
        		record['ward'] =  d.attrib['class']
        		record['time'] = d[0].text
        		record['number'] = d[1].text
        		record['tail'] = d[2].text
        		record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
        		msg = record['time'].replace('...',':') + space + record['number'] +space + record['tail']
        		messages.append(msg)

	tweet = random.choice(messages)
    	try:
    		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    		auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    		api = tweepy.API(auth)
    		api.update_status(tweet)
    		return True
   	except Exception, e:
   			print 'Failed to send tweet: %s' % tweet, e
    			return False

#landspitali_tweet()
#import cloud
#cloud.cron.register(landspitali_tweet, 'landspitali', '*/60 * * * *',_type = 's1')
#landspitali_tweet()