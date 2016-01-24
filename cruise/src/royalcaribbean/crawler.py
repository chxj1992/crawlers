# -*- coding: utf-8 -*-

import re
import sys
import time

import requests
from bs4 import BeautifulSoup

from .. import db


class Crawler:
    def __init__(self):
        self.host = "http://www.royalcaribbean.com/ajax"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
            'Accept': 'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'utf-8,gbk;q=0.7,*;q=0.3',
            'Connection': 'close',
            'Cookie': open(sys.path[0] + "/src/royalcaribbean/cookie.txt").read().strip(),
            'Referer': self.host
        }

    def run(self, page):
        url = self.host + '/cruises/searchbody?action=update&currentPage=' + str(page)
        content = requests.get(url, headers=self.headers).text

        soup = BeautifulSoup(content, 'lxml')
        results = soup.find_all("div", class_="search-result")

        if len(results) == 0:
            return False

        for row in results:
            cruise = {}
            title_elem = row.find(class_="search-result-top").find("h3").get_text(strip=True)
            cruise['title'] = re.compile(r'(\d.*)').findall(title_elem)[0]
            cruise['ship_name'] = row.find(class_="cruise-ship").find("strong").get_text(strip=True)
            cruise['duration'] = re.compile(r'^\d+').findall(cruise['title'])[0]
            cruise['departure_port'] = row.find(class_="cruise-details").find("strong").get_text(strip=True).split(
                    ",").pop(0)

            detail_url = self.host + '/cruise/inlinepricing/' + row.find(class_="cruise-detail-link cta-link").get(
                    "href").split("/").pop()

            self.get_detail(detail_url, cruise)

        return True

    def get_detail(self, url, cruise):
        res = requests.get(url, headers=self.headers).json()

        data = []
        price_pattern = re.compile(r'^\$(\d+)')
        for row in res['inlinePricing']['rows']:
            departure_time = int(time.mktime(time.strptime(row['dateLabel'], "%a - %d %b %Y")))
            inside = 0 if (row['priceItems'][0]['price'] is None) else \
                price_pattern.findall(row['priceItems'][0]['price'].replace(',', ''))[0]
            ocean_view = 0 if (row['priceItems'][1]['price'] is None) else \
                price_pattern.findall(row['priceItems'][1]['price'].replace(',', ''))[0]
            balcony = 0 if (row['priceItems'][2]['price'] is None) else \
                price_pattern.findall(row['priceItems'][2]['price'].replace(',', ''))[0]
            suite = 0 if (row['priceItems'][3]['price'] is None) else \
                price_pattern.findall(row['priceItems'][3]['price'].replace(',', ''))[0]

            data.append("('royalcaribbean', '" + \
                        str(res['packageId']) + \
                        "', '" + cruise['title'] + \
                        "', '" + cruise['ship_name'] + \
                        "', '" + str(cruise['duration']) + \
                        "', '" + cruise['departure_port'] + \
                        "', FROM_UNIXTIME(" + str(departure_time)+ \
                        "), '" + str(inside) + \
                        "', '" + str(ocean_view) + \
                        "', '" + str(balcony) + \
                        "', '" + str(suite) + \
                        "', '" + str(0) + \
                        "')")

        db.save(data)
        print cruise['title'].encode('utf-8') + ' Done! '
