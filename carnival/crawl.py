# encoding=utf-8

import json
import re
import time
import urllib2

import db


class Crawl:
    def __init__(self):
        self.host = "http://www.carnival.com/BookingEngine/SailingSearch/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
            'Accept': 'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'utf-8,gbk;q=0.7,*;q=0.3',
            'Connection': 'close',
            'Referer': self.host
        }

    def getListPage(self, page):
        url = self.host + 'Get?pageSize=100&pageNumber=' + str(page)
        req = urllib2.Request(url, headers=self.headers)
        res = json.loads(urllib2.urlopen(req).read())

        if len(res['Itineraries']) == 0:
            return False

        for itinerary in res['Itineraries']:
            self.saveItinerary(itinerary)

        return True

    def saveItinerary(self, itinerary):

        data = []
        pricePattern = re.compile(r'^\$(\d+)')
        for sailing in itinerary['Sailings']:
            departureTime = int(time.mktime(time.strptime(sailing['SailDateMMddyyyyInv'], "%m%d%Y")))
            inside = 0 if len(pricePattern.findall(sailing['INPriceText'])) == 0 else \
                pricePattern.findall(sailing['INPriceText'].replace(',', ''))[0]
            oceanView = 0 if len(pricePattern.findall(sailing['OVPriceText'])) == 0 else \
                pricePattern.findall(sailing['OVPriceText'].replace(',', ''))[0]
            balcony = 0 if len(pricePattern.findall(sailing['BAPriceText'])) == 0 else \
                pricePattern.findall(sailing['BAPriceText'].replace(',', ''))[0]
            suite = 0 if len(pricePattern.findall(sailing['STPriceText'])) == 0 else \
                pricePattern.findall(sailing['STPriceText'].replace(',', ''))[0]

            data.append("('carnival', '" + \
                        str(itinerary['ItineraryCode']) + \
                        "', '" + itinerary['ItnDescriptionText'] + \
                        "', '" + itinerary['ShipText'] + \
                        "', '" + str(itinerary['DurationDays']) + \
                        "', '" + itinerary['PortList'][0] + \
                        "', FROM_UNIXTIME(" + str(departureTime) + \
                        "), '" + str(inside) + \
                        "', '" + str(oceanView) + \
                        "', '" + str(balcony) + \
                        "', '" + str(suite) + \
                        "', '" + str(int(sailing['LowestPrice'])) + \
                        "')")

        db.save(data)
        print itinerary['ItnDescriptionText'] + ' Done! '
