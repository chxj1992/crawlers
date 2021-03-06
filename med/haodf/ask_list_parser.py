#!/usr/bin/python
# encoding: utf-8

import re
import sys

import requests
from bs4 import BeautifulSoup, NavigableString

import db
from med.thread import MyThread

reload(sys)
sys.setdefaultencoding('utf8')

ThreadNum = 10


class AskListParser:
    def __init__(self, base_url, section, tag, proxies=None):
        self.base_url = base_url
        self.section = section
        self.tag = tag
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        }
        self.proxies = proxies

    def run(self):
        threads = []

        for i in range(1, ThreadNum + 1):
            thread = MyThread(i, self, ThreadNum)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def get_list(self, page):
        url = self.base_url + str(page) + '.htm'
        if db.get_url(url) is not None:
            print 'ask list ' + url + ' exists'
            return True

        content = requests.get(url, headers=self.headers, proxies=self.proxies).text
        soup = BeautifulSoup(content, 'lxml')
        results = soup.select('.bbd_c > .advise_box_con')

        print 'inquiries : ' + str(results)

        if len(results) == 0:
            return False

        for row in results:
            text = ''.join([x for x in row.contents if isinstance(x, NavigableString)])
            match = re.compile(u'([\u7537\u5973]),(\d+)岁').findall(text)
            age = 0
            gender = 0
            if len(match) == 1:
                gender = 1 if match[0][0] == '男' else 2
                age = match[0][1]

            sql = 'INSERT INTO inquiries(`content`, `section`, `tag`, `gender`, `age`) VALUES (%s, %s, %s, %s, %s)'
            db.execute(sql, [text, self.section, self.tag, gender, age])

        db.save_url(url)
        return True


askListParser = AskListParser('http://www.haodf.com/jibing/fashao/zixun-', '儿科', '发烧')
askListParser.run()
