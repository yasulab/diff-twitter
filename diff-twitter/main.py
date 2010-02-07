#!/usr/bin/env python
# -*- coding:utf-8 -*-

#import datetime
#from datetime import datetime
import cgi
import os
import re
import base64
import urllib2
import twitter
import difflib
#import filecmp
import wsgiref.handlers

from urllib2 import Request, urlopen, URLError, HTTPError
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

fpList = []
url2html = {"url": "html"}

def my_twitter_api_init(self,
                        username=None,
                        password=None,
                        input_encoding=None,
                        request_headers=None):
    """overriding twitter.Api.__init__ method not to use FS cache.
    """
    import urllib2
    from twitter import Api
    self._cache = None

    self._urllib = urllib2
    self._cache_timeout = Api.DEFAULT_CACHE_TIMEOUT
    self._InitializeRequestHeaders(request_headers)
    self._InitializeUserAgent()
    self._InitializeDefaultParameters()
    self._input_encoding = input_encoding
    self.SetCredentials(username, password)
twitter.Api.__init__ = my_twitter_api_init

def br():
    print "<br>"

def readFile(filename):
    input = open(filename, "r")
    return input.read()

def readFileAsList(filename):
    input = open(filename, "r")
    return input.read().splitlines()

def saveHtml(html):
    fd = open("./html.txt", "w")
    fd.write(html)
    fd.close
    
def tweet(str):
    # If you don't know this password, please let admin know.
    api = twitter.Api("diff_bot", "???")
    str
    print "tweet: " + str.decode('shift-jis')
    status = api.PostUpdate(str.decode('shift-jis'))
    print status
    br()
    print "hogehoge\n"
        
def diff(oldStr, newStr):
    str1 = oldStr.splitlines()
    str2 = newStr.splitlines()
    strList = []
    
    for i,buf in enumerate(difflib.ndiff(str1, str2)):
        print "count: %s" % i
        if(buf.startswith("+ ") and len(buf) > 3):
            strList.append(buf.lstrip("+ "))
            #print "tweet: " + buf.lstrip("+ ").decode('shift-jis')
            #status = api.PostUpdate(buf.lstrip("+ ").decode('shift-jis'))
            #print "status: " + status
    print "Done to append.\nstrList: ",
    print strList
    return strList

urlList = readFile("./url_list.txt").splitlines()
for tmp in urlList:
    print "get URL: " + tmp
        
for i,url in enumerate(urlList):
    print "Search URL: " + url
    try:
        response = urlfetch.fetch(url)
    except urlfetch.DownloadError, e:
        print "DownloadError: " + e.read()
        continue
    except:
        print "Unexpected Error."
        continue
                
    if(response.status_code != 200):
        # if cannot get html correctly
        print "Cannot get html of URL: " + url
        continue

    #html = response.read()
    html = response.content
    if(url in url2html.keys()):
        # if same URL exists
        print "Found same URL in url2html."
        oldHtml  = readFile("./html.txt")
        # tweet diff if exists
        tweetList = diff(olHtml, html)
        oldHtml = html
        #saveHtml(oldHtml)
                
        #print "tweetList: ",
        for tweet_word in tweetList:
            print "tweet: " + tweet_word
            tweet(tweetList)
                
    else:
        # if same URL does not exist
        print "Add new URL("+url+") and its Html into url2html."
        url2html[url] = html
        #saveHtml(html)
               
    #self.redirect('/')



class MainHandler(webapp.RequestHandler):            
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf8'
        self.response.out.write('<html><body><strong>[Debug Output]</strong><br></body></html>')
        

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],debug=True)
    wsgiref.handlers.CGIHandler().run(application)
    tweet("test")

if __name__ == '__main__':
    main()  
