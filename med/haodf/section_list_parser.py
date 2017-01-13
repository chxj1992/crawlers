#!/usr/bin/python
# encoding: utf-8

import sys

import requests
from bs4 import BeautifulSoup
from med.haodf.jibing_list_parser import JibingListParser

from med.haodf import db

reload(sys)
sys.setdefaultencoding('utf8')


class SectionListParser:
    def __init__(self, url, proxies):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        }
        self.proxies = proxies

    def run(self):
        if db.get_url(self.url) is not None:
            print 'category ' + self.url + ' exists'
            return True

        content = requests.get(self.url, headers=self.headers, proxies=self.proxies).text
        soup = BeautifulSoup(content, 'lxml')
        results = soup.select('.ksbd a')

        print 'sections : ' + str(results)

        if len(results) == 0:
            return False

        for row in results:
            section = row.get_text().strip()
            url = row.attrs['href'].strip()
            JibingListParser('http://www.haodf.com' + url, section, self.proxies).run()

        db.save_url(self.url)
        return True

# sectionListParser = SectionListParser('http://www.haodf.com/jibing/xiaoerke/list.htm')
# sectionListParser.run()
