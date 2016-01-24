# encoding=utf-8

import re
import time

import requests

from .. import db


class Crawler:
    def __init__(self):
        self.host = "http://www.carnival.com/BookingEngine/SailingSearch/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
            'Accept': 'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'utf-8,gbk;q=0.7,*;q=0.3',
            'Connection': 'close',
            'Referer': self.host
        }

    def run(self, page):
        url = self.host + 'Get?pageSize=100&pageNumber=' + str(page)
        res = requests.get(url, headers=self.headers).json()

        if len(res['Itineraries']) == 0:
            return False

        for itinerary in res['Itineraries']:
            self.save_itinerary(itinerary)

        return True

    @staticmethod
    def save_itinerary(itinerary):
        data = []
        price_pattern = re.compile(r'^\$(\d+)')
        for sailing in itinerary['Sailings']:
            departure_time = int(time.mktime(time.strptime(sailing['SailDateMMddyyyyInv'], "%m%d%Y")))
            inside = 0 if len(price_pattern.findall(sailing['INPriceText'])) == 0 else \
                price_pattern.findall(sailing['INPriceText'].replace(',', ''))[0]
            ocean_view = 0 if len(price_pattern.findall(sailing['OVPriceText'])) == 0 else \
                price_pattern.findall(sailing['OVPriceText'].replace(',', ''))[0]
            balcony = 0 if len(price_pattern.findall(sailing['BAPriceText'])) == 0 else \
                price_pattern.findall(sailing['BAPriceText'].replace(',', ''))[0]
            suite = 0 if len(price_pattern.findall(sailing['STPriceText'])) == 0 else \
                price_pattern.findall(sailing['STPriceText'].replace(',', ''))[0]

            data.append("('carnival', '" + \
                        str(itinerary['ItineraryCode']).encode('utf8') + \
                        "', '" + itinerary['ItnDescriptionText'].encode('utf8') + \
                        "', '" + itinerary['ShipText'].encode('utf8') + \
                        "', '" + str(itinerary['DurationDays']).encode('utf8') + \
                        "', '" + itinerary['PortList'][0].encode('utf8') + \
                        "', FROM_UNIXTIME(" + str(departure_time).encode('utf8') + \
                        "), '" + str(inside).encode('utf8') + \
                        "', '" + str(ocean_view).encode('utf8') + \
                        "', '" + str(balcony).encode('utf8') + \
                        "', '" + str(suite).encode('utf8') + \
                        "', '" + str(int(sailing['LowestPrice'])).encode('utf8') + \
                        "')")

        db.save(data)
        print itinerary['ItnDescriptionText'] + ' Done! '
