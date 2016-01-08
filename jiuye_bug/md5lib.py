#encoding=utf8

import urllib2
import urllib
import re
import socket

class Cracker:

    def __init__(self):
        self.cracker = [self.md5Cn, self.md5Hk, self.freemd5]
        self.md5CnSand = ''
        self.md5CnToken = ''
        self.crackerIndex = 0
        self.count = 0


    def crack(self, md5):
        for i in range(0,len(self.cracker)):
            self.crackerIndex = i
            ret = self.cracker[i](md5) 
            if ( ret != '' ) :
                return ret

        print "Not Found"
        return ''


    #http://cn.freemd5.com/index.php
    def freemd5(self, md5):
        url = 'http://cn.freemd5.com/index.php'
        data = {'md5':md5, 'crackencryption':'decryption'} 
        content = self.post(url, data)
        pwPattern = re.compile(r'MD5.*<br>(\w+)</h2>')
        password = pwPattern.findall(content)
        if ( len(password) != 0 ): 
            print 'Found in freemd5'
            return password[0]
        return ''


    #http://www.md5.hk/
    def md5Hk(self, md5):
        url = 'http://www.md5.hk/'
        data = {'md5_str':md5, 'button':'MD5在线解密'} 
        content = self.post(url, data).decode('gbk').encode('utf8')
        pwPattern = re.compile(r'ShowInfo.*>(\w+)')
        password = pwPattern.findall(content)
        if ( len(password) != 0 ): 
            print 'Found in md5Hk'
            return password[0]
        return ''


    #http://www.md5.com.cn/
    def md5Cn(self, md5):
        self.count = self.count + 1
        if( self.md5CnToken == '' or self.count>10 ):
            self.count = 1
            self.getMd5CnToken()
        url = 'http://www.md5.com.cn/md5reverse'
        data = {'md':md5, 'sand':self.md5CnSand, 'token':self.md5CnToken, 'submit':'MD5 Crack'} 
        content = self.post(url, data)
        pwPattern = re.compile(r'Result:.*\n.*<b.*>(\w+)</b>')
        password = pwPattern.findall(content)
        if ( len(password) != 0 ): 
            print 'Found in md5Cn'
            return password[0]
        return ''


    def getMd5CnToken(self):
        url = 'http://www.md5.com.cn/md5'
        content = self.post(url, {})
        sandPattern = re.compile(r'name="sand" value="(\d+)"')
        tokenPattern = re.compile(r'name="token" value="(\w+)"')
        sand = sandPattern.findall(content)
        token = tokenPattern.findall(content)
        if( len(sand) > 0 and len(token) > 0 ):
            self.md5CnSand = sand[0]
            self.md5CnToken = token[0]


    def post(self, url, data):  
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
                   'Accept':'text/html;q=0.9,*/*;q=0.8',
                   'Accept-Charset':'utf-8,gbk;q=0.7,*;q=0.3',
                   'Connection':'close',
                   'Referer':url}
        try:
            req = urllib2.Request(url, urllib.urlencode(data), headers)  
            response = urllib2.urlopen(req, timeout=10)  
            return response.read() 
        except urllib2.HTTPError, e:
            print "Http Error!"
            self.cracker.remove(self.crackerIndex)
            return ''
        except socket.timeout, e:
            print "Timeout!"
            return ''
        except urllib2.URLError, e:
            print "Skip"
            return ''

