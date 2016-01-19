# encoding=utf-8
import json
import urllib2

import db


class Crawl:

    def __init__(self):
        self.host = "http://weibo.chxj.name/"
        self.nextCursor = "0" 
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
            'Accept': 'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'utf-8,gbk;q=0.7,*;q=0.3',
            'Connection': 'close',
            'Cookie': 'authuser=Mjc5NDY0NzI2NToxNDEzNDg2MDAxOjA1NGE1MjY1ZmFiMDMyZDA4OGM2NmE4OGE5YzVlNzRm',
            'Referer': self.host}


    def get(self, url):
        req = urllib2.Request(url, headers=self.headers)
        content = urllib2.urlopen(req).read()
        return content


    def friends(self):
        url = self.host + '/friends'
        content = self.get(url)
        print content

    def followers(self):
        url = self.host + '/followers?cursor='+str(self.nextCursor)
        content = json.loads(self.get(url))
        self.nextCursor = content['next_cursor']
        data = []
        for user in content['users']:
            data.append((user['id'], user['screen_name'], user['province'], user['city'], user['location'], user['bi_followers_count']))

        sql = "REPLACE INTO followers(uid, screen_name, province, city, location, bi_followers_count) VALUES (%s, %s, %s, %s, %s, %s)"
        db.execute(sql, data)


c = Crawl()
c.followers()

while (c.nextCursor != 0):
    print c.nextCursor
    c.followers()


