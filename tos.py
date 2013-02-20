# -*- coding: utf-8 -*-

#_profile=True

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
BITLY_ACCESS_TOKEN = ''

import tweepy
import datetime
import requests
import random
import lxml.html
import bitly_api

def smart_truncate(content, length=110, suffix='[...]'):
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0]+suffix

def tos_tweeter():
        randomint = random.randint(1,7689)
        html = requests.get('http://tos.sky.is/tos/to/word/isl/%s/' % randomint).text

        root = lxml.html.fromstring(html)
        for node in root.cssselect("sup"): #drop footnotes
            node.drop_tree()
        try:
            word = root.xpath('//div[@class="word_title"]')
            word_isl = word[0][0].text[:1].upper() + word[0][0].text[1:]
            kyn = word[0][0].tail.strip()
            word_definition = root.xpath('//div[@class="word_definition"]')[0].text_content()
            enska = root.xpath('//div[@class="word_detail"]/*[text()="Enska:"]/..')[0].text_content().replace('Enska:','(e.')
            if kyn != '':
                 strengur = word_isl +' ('+kyn+')'
            else:
                 strengur = word_isl
            strengur = strengur + ' '+ enska + '). ' + word_definition
            strengur = smart_truncate(strengur)
            c = bitly_api.Connection(access_token=BITLY_ACCESS_TOKEN)
            shorturl =  c.shorten('http://tos.sky.is/tos/to/word/isl/%s/' % randomint)['url']
            strengur = strengur + ' ' +shorturl

        except Exception, e:
            tos_tweeter()
        try:
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
            api = tweepy.API(auth)
            api.update_status(strengur)
            return True
        except Exception, e:
            tos_tweeter()
#import cloud
#cloud.cron.register(tos_tweeter, 'tos_tweeter', '0 9 * * *',_type = 's1',_max_runtime=3)
