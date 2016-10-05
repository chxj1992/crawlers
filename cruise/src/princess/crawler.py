# -*- coding: utf-8 -*-

import re
import time

import requests
from bs4 import BeautifulSoup

from .. import db


def match_price(row, index):
    price_elem = row.find("td", class_=index)
    if price_elem is None:
        return 0
    match = re.compile(r'\d+').findall(price_elem.get_text(strip=True).replace(',', ''))
    return 0 if (len(match) == 0) else match[0]


def save(data):
    sql = 'REPLACE INTO cruises(project, itinerary_id, title, ship_name, duration, departure_port, departure_time, \
            inside, oceanview, balcony, suite, is_lowest_price) VALUES ' + ','.join(data)
    db.execute(sql)


class Crawler:
    def __init__(self):
        self.host = "http://www.princess.com/find/pagination.do"
        self.headers = {
            'Cookie': 'Click to edit=; loc:=; loc:0=; ; ak_bmsc=E7BF4D47580C177E1FE725AE198CF88D17C96696EE7F0000BC09DC57F244781A~plouF4RcSIA6wPHEisGpMrx+FnluRFOJa7kfceyBVVGC9gwvpCv7GGOkdX7X6qHtOJ31suCHN1Sw8Fch22ws3oFWqoGHjATStKNRohQMYkaxPEdFJM4Y478QuhJwUUrYCEe33NQoS7Bf7rAiZG1aqQlfrS5zO1HfYIIdpZ68epXL/0u6brhcBPM+7ImIcL+ZFdEMbTOZGiKciL9qABAbYfzafRGPxbVzZhFDzhSX6cWno=; EG-S-ID=B2453f6d20-7742-4763-9ed1-d13c46947e4b; EG-U-ID=E698978b68-2e10-4f4f-adee-36514c28f362; mf_record_user=1; _ga=GA1.2.172208134.1474038208; mf_f3a02463-b43f-48da-9dcb-90e7d2f103b1=-1; __utma=169354720.172208134.1474038208.1474038208.1474038208.1; __utmb=169354720.6.10.1474038208; __utmz=169354720.1474038208.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aam_uuid=86114146738351184951998596534478988654; COOKIE_CHECK=YES; __utmc=169354720; getLocale=%7B%22specialOffers%22%3A%22true%22%2C%22status%22%3A%22%22%2C%22country%22%3A%22HK%22%2C%22countryPhone%22%3A%22(852)%202952-8088%22%2C%22isEU%22%3A%22false%22%2C%22brochures%22%3A%22true%22%2C%22lastUpdated%22%3A1474039574820%7D; JSESSIONID=0001Qb-WdMYufydOZYTDHvwfxko:181iip1is; _fipa_=CAN; _fipz_=610000; _fipc_=us; _fby_site_=1%7Cprincess.com%7C1474038224%7C1474038224%7C1474038224%7C1474039708%7C1%7C12%7C12; optimizelySegments=%7B%22338835449%22%3A%22direct%22%2C%22339434131%22%3A%22gc%22%2C%22339521333%22%3A%22false%22%2C%222201270270%22%3A%22none%22%2C%223383280747%22%3A%22New%22%2C%225277922587%22%3A%22true%22%7D; optimizelyEndUserId=oeu1474038208230r0.2702973990340962; booking_engine_used=PCDIR; search_counter=7; loc=SH3HZ63UPZQNUOGZLJQKLURWZXPW3KDUBKWMBVT4H6FJDLMJTTQIFTQXWE7GFFHKVNVKUHTT4CXOKNN36JX7PFSA2NNFBPB7RB3B5U3UML2DSPMQUH4Q; _aeu=QCQ=; _aes=QSE=; dl.VoyageCode=0:; EG-S-ID=B2453f6d20-7742-4763-9ed1-d13c46947e4b; EG-U-ID=E698978b68-2e10-4f4f-adee-36514c28f362; mf_f3a02463-b43f-48da-9dcb-90e7d2f103b1=-1; COOKIE_CHECK=YES; _fipc_=cn; _fipa_=CAN; _fipz_=610000; loc=SH3HZ63UPZQNUOGZLJQKLURWZXPW3KDUBKWMBVT4H6FJDLMJTTQIFTQXWE7GFFHKVNVKUHTT4CXOKNN36JX7PFSA2NNFBPB7RB3B5U3UML2DSPMQUH4Q; JSESSIONID=0001lpGg1Dl1tvaR-7sTqx9QSUA:181iip1is; getLocale=%7B%22specialOffers%22%3A%22true%22%2C%22status%22%3A%22US%22%2C%22country%22%3A%22US%22%2C%22countryPhone%22%3A%221-800-774-6237%22%2C%22isEU%22%3A%22false%22%2C%22brochures%22%3A%22true%22%2C%22lastUpdated%22%3A1475677802185%7D; mf_record_user=1; _aeu=QCQ=; _aes=QSE=; dl.VoyageCode=0:; _dc_gtm_UA-4086206-54=1; __utmt_princess=1; __utmt=1; _gat_UA-4086206-54=1; __atuvc=1%7C40; __atuvs=57f50e6ed05fd46a000; booking_engine_used=PCDIR; search_counter=8; _ga=GA1.2.172208134.1474038208; spo=QBJFQGDPMX265UMGHAH7WTU6YU; aam_uuid=86114146738351184951998596534478988654; _fby_site_=1%7Cprincess.com%7C1474038224%7C1474038224%7C1475677806%7C1475677823%7C2%7C3%7C15; __utma=169354720.172208134.1474038208.1474038208.1474038208.1; __utmb=169354720.9.9.1475677821008; __utmc=169354720; __utmz=169354720.1474038208.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); optimizelySegments=%7B%22338835449%22%3A%22referral%22%2C%22339434131%22%3A%22gc%22%2C%22339521333%22%3A%22false%22%2C%222201270270%22%3A%22none%22%2C%223383280747%22%3A%22Returning%22%2C%225277922587%22%3A%22true%22%7D; optimizelyEndUserId=oeu1474038208230r0.2702973990340962; optimizelyBuckets=%7B%227268510386%22%3A%220%22%7D'
        }

    def run(self, page):
        size = 100
        url = self.host + '?searchCriteria.currency=USD&searchCriteria.startIndex=' + str((page - 1) * size) + '&searchCriteria.endIndex=' + str(
                page * size)
        content = requests.get(url, headers=self.headers).text
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
