#encoding=utf-8
import urllib
import urllib2
import re
import socket
import mechanize

class Crawl:

    def __init__(self):
        self.host = "http://weibo.com"

    def get(self, url):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [ ('User-Agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'),
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
            #'Accept-Encoding': 'deflate,sdch',
            ('Accept-Language', 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'),
            ('Connection', 'keep-alive'),
            ('Cookie', open("cookie.txt").read().strip()),
            ('Referer', self.host)]

        try:
            return br.open(url, timeout=30).read()
        except socket.timeout, e:  
            print "timeout!\n"
            return self.get(url)


    def run(self, url):
        content = self.get(url)
        print content


