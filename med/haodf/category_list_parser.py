#!/usr/bin/python
# encoding: utf-8

import sys

import requests
from bs4 import BeautifulSoup
from med.haodf.section_list_parser import SectionListParser

reload(sys)
sys.setdefaultencoding('utf8')

proxies = {
    # 'http': helper.get_http_proxy()
}


class CategoryListParser:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        }

    def run(self):
        url = 'http://www.haodf.com/jibing/list.htm'
        content = requests.get(url, headers=self.headers, proxies=proxies).text
        soup = BeautifulSoup(content, 'lxml')
        results = soup.select('.kstl a')

        print 'categories : ' + str(results)

        if len(results) == 0:
            return False

        for row in results:
            href = row.attrs['href'].strip()
            url = 'http://www.haodf.com' + href
            SectionListParser(url, proxies).run()

        return True


categoryListParser = CategoryListParser()
categoryListParser.run()
