# -*- coding: utf-8 -*-

import re
import time

import requests
from bs4 import BeautifulSoup

from .. import db


def match_price(row, index):
    match = re.compile(r'\d+').findall(row.find("td", class_=index).get_text(strip=True).replace(',', ''))
    return 0 if (len(match) == 0) else match[0]


def save(data):
    sql = 'REPLACE INTO cruises(project, itinerary_id, title, ship_name, duration, departure_port, departure_time, \
            inside, oceanview, balcony, suite, is_lowest_price) VALUES ' + ','.join(data)
    db.execute(sql)


class Crawler:
    def __init__(self):
        self.host = "http://www.princess.com/find/pagination.do"

    def run(self, page):
        size = 100
        url = self.host + '?searchCriteria.startIndex=' + str((page - 1) * size) + '&searchCriteria.endIndex=' + str(
                page * size)
        content = requests.get(url).text

        soup = BeautifulSoup(content, 'lxml')
        results = soup.find_all("div", class_="result")

        if len(results) == 0:
            return False

        for row in results:
            cruise = self.parse_row(row)
            save(self.build_sql(row, cruise))
            print cruise['title'].encode('utf-8') + ' Done! '

        return True

    @staticmethod
    def parse_row(row):
        cruise = {
            'itinerary_id': row.get('id'),
            'title': row.find(class_="cruise-name").get_text(strip=True),
            'ship_name': row.find(class_="ship-info").find(class_="ship").get_text(strip=True),
            'duration': int(row.find(class_="cruise-days").find('div').get_text(strip=True)),
            'departure_port': row.find(class_="ports-info").find(class_="port").get_text(strip=True),
            'inside': match_price(row, "interior"),
            'ocean_view': match_price(row, "oceanview"),
            'balcony': match_price(row, "balcony"),
            'suite': match_price(row, "suite")
        }

        return cruise

    @staticmethod
    def build_sql(row, cruise):
        data = []
        departure_time_list = row.select('option[data-tour]')
        if len(departure_time_list) == 0:
            departure_time_list = [row.find(class_="depart-date")]

        for departure_time in departure_time_list:
            departure_time = int(time.mktime(time.strptime(departure_time.get_text(strip=True), "%a, %b %d, %Y")))
            data.append("('princess', '" + \
                        str(cruise['itinerary_id']) + \
                        "', '" + cruise['title'] + \
                        "', '" + cruise['ship_name'] + \
                        "', '" + str(cruise['duration']) + \
                        "', '" + cruise['departure_port'] + \
                        "', FROM_UNIXTIME(" + str(departure_time) + \
                        "), '" + str(cruise['inside']) + \
                        "', '" + str(cruise['ocean_view']) + \
                        "', '" + str(cruise['balcony']) + \
                        "', '" + str(cruise['suite']) + \
                        "', '" + str(0) + \
                        "')")

        return data


if __name__ == "__main__":
    c = Crawler()
    c.run(1)
