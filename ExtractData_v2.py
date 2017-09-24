# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 12:51:55 2017

@author: Sudath
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import re
import time
import csv
import pprint as pp
from collections import OrderedDict



def tweetscrape(startdate, enddate, numscroll):


    numscroll = numscroll
    startdate=startdate
    enddate=enddate
    #executable_path = path_to_chromedriver
    #path_to_chromedriver = 'C:/Users/Gayathri/Desktop/#sem 2/Applied project/Python Files'            # change path as needed
    browser = webdriver.Chrome()

    #Different combinations of keywords
    #url_initial = u'https://twitter.com/search?l=en&q=trump%20OR%20hilary%20OR%20clinton%20OR%20%23MAGA%20OR%20%23potus%20OR%20elections2016%20OR%20%23imwithher%20near%3A%22Phoenix%2C%20AZ%22%20within%3A150mi%20since%3A2016-09-01%20until%3A2016-11-11&src=typd&lang=en'
    #Phoenix
    #url=u'https://twitter.com/search?q=trump%20OR%20donaldtrump%20OR%20hilaryclinton%20OR%20clinton%20OR%20MAGA%20OR%20POTUS%20OR%20elections2016%20OR%20opinionpolls%20OR%20%E2%80%9CI%27m%20with%20her%E2%80%9D%20OR%20%23imwithher%20OR%20%23MAGA%20OR%20%23POTUS%20lang%3Aen%20since%3A2016-09-01%20until%3A2016-11-11%20near%3A%22Phoenix%2C%20AZ%22%20within%3A150mi&src=typd&lang=en'
    #No_location
    #url=u'https://twitter.com/search?q=trump%20OR%20donaldtrump%20OR%20hilaryclinton%20OR%20clinton%20OR%20MAGA%20OR%20POTUS%20OR%20elections2016%20OR%20opinionpolls%20OR%20%E2%80%9CI%27m%20with%20her%E2%80%9D%20OR%20%23imwithher%20OR%20%23MAGA%20OR%20%23POTUS%20lang%3Aen%20since%3A2016-11-01%20until%3A2016-11-11&src=typd&lang=en'
    #url=u'https://twitter.com/search?q=trump%20OR%20donaldtrump%20OR%20hilaryclinton%20OR%20clinton%20OR%20MAGA%20OR%20POTUS%20OR%20elections2016%20OR%20opinionpolls%20OR%20%E2%80%9CI%27m%20with%20her%E2%80%9D%20OR%20%23imwithher%20OR%20%23MAGA%20OR%20%23POTUS%20lang%3Aen%20since%3A2016-09-01%20until%3A2016-09-01&src=typd&lang=en'
    url=u'https://twitter.com/search?l=en&q=donaldtrump%20OR%20trump%20OR%20hilaryclinton%20OR%20clinton%20OR%20%23MAGA%20OR%20%23potus%20OR%20elections2016%20OR%20%23imwithher%20OR%20%23makeamericagreatagain%20OR%20%23notmypresident'+'%20since%3A'+startdate+'%20until%3A'+enddate+'&src=typd&lang=en'
    print(url)

    #function to handle dynamic page content loading - using Selenium
    def twt_scroller(url):

        browser.get(url)

        #define initial page height for 'while' loop
        lastHeight = browser.execute_script("return document.body.scrollHeight")
        i=1
        while True:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #define how many seconds to wait while dynamic page content loads
            time.sleep(1)
            newHeight = browser.execute_script("return document.body.scrollHeight")
            i=i+1
            if newHeight == lastHeight or i==numscroll:
                break
            else:
                lastHeight = newHeight

        html = browser.page_source

        return html




    #function to handle/parse HTML and extract data - using BeautifulSoup
    def blogxtract(url):

        #regex patterns
        problemchars = re.compile(r'[\[=\+/&<>;:!\\|*^\'"\?%$@)(_\,\.\t\r\n0-9-—\]]')
        prochar = '[(=\-\+\:/&<>;|\'"\?%#$@\,\._)]'
        crp = re.compile(r'MoreCopy link to TweetEmbed Tweet|Reply')
        wrd = re.compile(r'[A-Z]+[a-z]*')
        dgt = re.compile(r'\d+')
        url_finder = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        retweet = re.compile(r"(?<=Retweet:)(.*)(?=', u'R)")
        fave = re.compile(r"(?<=Like:)(.*)(?=', u'Liked)")

        blog_list = []

        #set to global in case you want to play around with the HTML later
        global soup

        #call dynamic page scroll function here
        soup = BeautifulSoup(twt_scroller(url), 'html.parser')
        #print("printing html",soup)


        for i in soup.find_all('li', {"data-item-type":"tweet"}):


                user = (i.find('span', {'class':"username js-action-profile-name"}).get_text() if i.find('span', {'class':"username js-action-profile-name"}) is not None else "")
                link = ('https://twitter.com' + i.small.a['href'] if i.small is not None else "")
                date = (i.small.a['title'] if i.small is not None else "")
                popular = (i.find('div', {'class': "ProfileTweet-actionList js-actions"}).get_text().replace('\n','') if i.find('div', {'class': "ProfileTweet-actionList js-actions"}) is not None else "")
                print((i.p.get_text().lower()).strip().replace('\n',''))
                text = ((i.p.get_text().lower()).strip().replace('\n','').replace("'",'') if i.p is not None else "")
                popular_text = [i + ':' + j  if len(dgt.findall(popular)) != 0 else '' for i, j in zip(wrd.findall(crp.sub('', popular)), dgt.findall(popular))]


                #build dictionary
                blog_dict = {
                "header": "twitter_hashtag_" + url.rsplit('/',2)[1],
                "url": link,
                "user": user,
                "date": date,
                "popular": popular_text,
                #before text is stored URLs are removed - note: hash symbol is maintained to indicate hashtag term
                "blog_text": problemchars.sub('', url_finder.sub('', text)).encode('ascii','ignore'),
                "like_fave": (int(''.join(fave.findall(str(popular_text)))) if len(fave.findall(str(popular_text))) > 0 else ''),
                "share_rtwt": (int(''.join(retweet.findall(str(popular_text)))) if len(retweet.findall(str(popular_text))) > 0 else '')
                }

                blog_list.append(blog_dict)

        #error handling
        #except (AttributeError, TypeError, KeyError, ValueError):
            #print ("missing_value")

        print("tweets dict",blog_dict)
        #call csv writer function and output file
        writer_csv_3(blog_list)


        return pp.pprint(blog_list[0:2])



    #function to write CSV file
    def writer_csv_3(blog_list):

        #uses group name from URL to construct output file name
        file_out = "twitter_tweets_us_"+startdate+".csv".format(page = url.rsplit('/',2)[1])

        with open(file_out, 'w') as csvfile:

            writer = csv.writer(csvfile, lineterminator='\n', delimiter=',', quotechar='"')
            newrow = "test header"

            for i in blog_list:
                if len(i['blog_text']) > 0:
                    #newrow = i['header'], i['url'], i['user'], i['date'], i["popular"], i['blog_text'], i["like_fave"], i["share_rtwt"]
                    newrow = i['url'], i['user'], i['date'],i['blog_text']

                    writer.writerow(newrow)
                else:
                    pass

         #tip the domino
    if __name__ == "__main__":
        blogxtract(url)

tweetscrape(startdate = "2016-08-07", enddate = "2016-08-08", numscroll = 3000)
