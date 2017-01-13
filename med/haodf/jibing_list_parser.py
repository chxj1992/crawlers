#!/usr/bin/python
# encoding: utf-8

import sys

import requests
from bs4 import BeautifulSoup
from med.haodf.ask_list_parser import AskListParser

from med.haodf import db

reload(sys)
sys.setdefaultencoding('utf8')


class JibingListParser:
    def __init__(self, url, section, proxies):
        self.url = url
        self.section = section
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        }
        self.proxies = proxies

    def run(self):
        if db.get_url(self.url) is not None:
            print 'section ' + self.url + ' exists'
            return True

        content = requests.get(self.url, headers=self.headers, proxies=self.proxies).text
        soup = BeautifulSoup(content, 'lxml')
        results = soup.select('.m_ctt_green a')

        print 'tags : ' + str(results)

        if len(results) == 0:
            return False

        for row in results:
            href = row.attrs['href'].replace('.htm', '/zixun-').strip()
            tag = row.get_text().strip()

            url = 'http://www.haodf.com' + href
            if db.get_url(url) is not None:
                print 'jibing ' + url + ' exists'
                continue

            AskListParser(url, self.section, tag, self.proxies).run()
            db.save_url(url)

        db.save_url(self.url)
        return True

# jibingListParser = JibingListParser('http://www.haodf.com/jibing/erkezonghe/list.htm', '儿科')
# jibingListParser.run()
