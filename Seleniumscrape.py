# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 16:49:45 2017

@author: sudath
"""

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import datetime
import csv
st = time.strftime('%a %H:%M:%S')
search_words = "potus "
file_name = search_words#+str(st)+'.csv'

browser= webdriver.Chrome()
base_url=u'https://twitter.com/search?q='
query=u'potus%20OR%20hillary%20OR%20clinton%20OR%20donald%20OR%20trump%20OR%20elections%20since%3A2016-11-01%20until%3A2016-11-08%20%3A)&src=typd/'
url=base_url+query
browser.get(url)
time.sleep(1)

body=browser.find_element_by_tag_name('body')

for _ in range(1):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.3)

tweets=browser.find_elements_by_class_name('tweet-text')

for tweet in tweets:
    print(tweet.text)
temp = tweet.text

with open('potus.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ')
    spamwriter.writerow("\""+temp+"\"")

for tweet in tweets:
    print(tweet.text)
temp = tweet.text


