# -*- coding: utf-8 -*-

import urllib

import requests

from .. import db


class Crawler:
    def __init__(self):
        self.host = "https://www.travelocity.com/Cruise-Search/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
            'Accept': 'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'utf-8,gbk;q=0.7,*;q=0.3',
            'Connection': 'close',
            'Referer': self.host
        }

    def run(self, page):
        url = self.host + 'Results?page=' + str(page)
        res = requests.get(url, headers=self.headers).json()

        if 'errorMessage' in res:
            return False

        cruise_cards = res['cruiseCards']

        for cruise_card in cruise_cards:
            self.get_detail(cruise_card)

        return True

    @staticmethod
    def build_title(cruise_card):
        title = str(cruise_card['duration']) + '-night ' + cruise_card['destination'] + ' Cruise from ' + cruise_card[
            'startPort']
        if cruise_card['isRoundtrip']:
            title += ' (Roundtrip)'

        return title

    def build_detail_url(self, cruise_card):
        param = {}
        param['cruiseLineCode'] = cruise_card['cruiseLineCode']
        param['cruiseLineName'] = cruise_card['cruiseLineName']
        param['shipName'] = cruise_card['deepLinkShipName']
        param['itineraryId'] = str(cruise_card['itineraryId'])
        param['duration'] = str(cruise_card['duration'])
        param['isSponsoredListing'] = str(cruise_card['sponsoredListing'])
        param['departurePortName'] = cruise_card['startPort']

        return self.host + 'ItineraryDetails?' + urllib.urlencode(param)

    def get_detail(self, cruise_card):
        url = self.build_detail_url(cruise_card)
        title = self.build_title(cruise_card)
        res = requests.get(url, headers=self.headers).json()

        if not ('sailingYears' in res):
            raise Exception("sailing years lost!")

        data = []
        for sailing_year in res['sailingYears']:
            for sailing_month in sailing_year['sailingMonths']:
                for sailing_date in sailing_month['sailingDates']:
                    departure_time = int(sailing_date['departureTimeInMillis'] / 1000)
                    data.append("('travelocity', '" + \
                                str(cruise_card['itineraryId']).encode('utf8') + \
                                "', '" + title.encode('utf8') + \
                                "', '" + cruise_card['shipName'].encode('utf8') + \
                                "', '" + str(cruise_card['duration']).encode('utf8') + \
                                "', '" + cruise_card['startPort'].encode('utf8') + \
                                "', FROM_UNIXTIME(" + str(departure_time).encode('utf8') + \
                                "), '" + str(sailing_date['insideCabinPrice']).encode('utf8') + \
                                "', '" + str(sailing_date['oceanViewCabinPrice']).encode('utf8') + \
                                "', '" + str(sailing_date['balconyCabinPrice']).encode('utf8') + \
                                "', '" + str(sailing_date['suiteCabinPrice']).encode('utf8') + \
                                "', '" + str(int(sailing_date['isLowestPrice'])).encode('utf8') + \
                                "')")

        db.save(data)
        print title + ' Done! '
