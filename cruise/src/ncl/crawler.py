# -*- coding: utf-8 -*-

import re
import time

import requests
from bs4 import BeautifulSoup

from .. import db


def match_price(row, index):
    price_elem = row.find(attrs={"mappingcolumn": index})
    if price_elem is None:
        return 0
    price_pattern = re.compile(r'^\$(\d+)')
    match = price_pattern.findall(price_elem.find(class_="data-wrap").get_text(strip=True).replace(',', ''))

    return 0 if (len(match) == 0) else match[0]


def save(data):
    sql = 'REPLACE INTO cruises(project, itinerary_id, title, ship_name, duration, departure_port, departure_time, \
            inside, oceanview, balcony, suite, studio, spa, haven, is_lowest_price) VALUES ' + ','.join(data)
    db.execute(sql)


class Crawler:
    def __init__(self):
        self.host = "https://www.ncl.com/vacations"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
            'Accept': 'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'utf-8,gbk;q=0.7,*;q=0.3',
            'Connection': 'close',
            'Referer': self.host
        }

    def run(self, page):
        url = self.host + '?pageSize=20&currentPage=' + str(page)
        content = requests.get(url, headers=self.headers).text

        soup = BeautifulSoup(content, 'lxml')
        results = soup.find_all("section", class_="tripdetails")

        if len(results) == 0:
            return False

        for row in results:
            cruise = {}
            cruise['title'] = row.find(class_="titledetails").get_text(strip=True)
            cruise['ship_name'] = row.find(class_="shipname").find("strong").get_text(strip=True)
            duration_match = re.compile(r'^\d+').findall(cruise['title'])
            cruise['duration'] = 0 if len(duration_match) is 0 else duration_match[0]
            cruise['departure_port'] = row.find(class_="ports").find("strong").get_text(strip=True)
            cruise['itinerary_id'] = row.find(attrs={"name": "itineraryCode"}).get("value")

            detail_url = self.host + "/_/sailings?itineraryCode=" + cruise['itinerary_id']
            self.get_detail(detail_url, cruise)

        return True

    def get_detail(self, url, cruise):
        content = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(content, 'lxml')
        results = soup.find_all("ul", class_="resetgrid")

        data = []
        for row in results:
            studio = match_price(row, "STUDIO")
            inside = match_price(row, "INSIDE")
            ocean_view = match_price(row, "OCEANVIEW")
            balcony = match_price(row, "BALCONY")
            spa = match_price(row, "SPA")
            suite = match_price(row, "MINISUITE")
            haven = match_price(row, "HAVEN")

            datetime = row.find(class_='datepriceselector ').get('data-value').split(',')
            departure_time = int(time.mktime(time.strptime(datetime[0] + datetime[1], "%B %d %Y")))

            data.append("('ncl', '" + \
                        str(cruise['itinerary_id']) + \
                        "', '" + cruise['title'] + \
                        "', '" + cruise['ship_name'] + \
                        "', '" + str(cruise['duration']) + \
                        "', '" + cruise['departure_port'] + \
                        "', FROM_UNIXTIME(" + str(departure_time) + \
                        "), '" + str(inside) + \
                        "', '" + str(ocean_view) + \
                        "', '" + str(balcony) + \
                        "', '" + str(suite) + \
                        "', '" + str(studio) + \
                        "', '" + str(spa) + \
                        "', '" + str(haven) + \
                        "', '" + str(0) + \
                        "')")

        save(data)
        print cruise['title'].encode('utf-8') + ' Done! '


if __name__ == "__main__":
    c = Crawler()
    c.run(1)
