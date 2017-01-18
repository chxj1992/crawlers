#!/usr/bin/python
# encoding: utf-8

import re
import sys

import requests
from bs4 import BeautifulSoup

from med.haodf_doctor import db

reload(sys)
sys.setdefaultencoding('utf8')


class JibingListParser:
    def __init__(self, url, section):
        self.url = url
        self.section = section
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        }

    def run(self):
        if db.get_url(self.url) is not None:
            print 'section ' + self.url + ' exists'
            return True

        content = requests.get(self.url, headers=self.headers).text
        soup = BeautifulSoup(content, 'lxml')
        results = soup.select('.m_ctt_green a')

        if len(results) == 0:
            return False

        sql = "INSERT INTO jibing (`name`) VALUE (%s)"
        for row in results:
            href = row.attrs['href']
            jibing = re.compile(r'(\w+)\.htm').findall(href)[0]

            print jibing

            try:
                db.execute(sql, [jibing])
            except Exception:
                continue

        db.save_url(self.url)
        return True
