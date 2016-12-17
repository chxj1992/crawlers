#!/usr/bin/python
# encoding: utf-8

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Cookie': ''
}

content = requests.get('http://fang.vanke.com/ActivityTarget/Auction/798109?site=7', headers=headers).text

soup = BeautifulSoup(content, 'lxml')
token = soup.find('input', attrs={"name": "__RequestVerificationToken"}).get('value')

res = requests.post('http://fang.vanke.com/ActivityTarget/AddPrice',
                    {'id': 798109, 'site': 7, 'price': '60000.00', '__RequestVerificationToken': token},
                    headers=headers)

print(res.text)
