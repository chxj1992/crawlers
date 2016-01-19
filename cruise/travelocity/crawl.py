# encoding=utf-8

import json
import urllib
import urllib2

import db


class Crawl:
    def __init__(self):
        self.host = "https://www.travelocity.com/Cruise-Search/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
            'Accept': 'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'utf-8,gbk;q=0.7,*;q=0.3',
            'Connection': 'close',
            'Referer': self.host
        }

    def getListPage(self, page):
        url = self.host + 'Results?page=' + str(page)
        req = urllib2.Request(url, headers=self.headers)
        res = json.loads(urllib2.urlopen(req).read())

        if (res.has_key('errorMessage')):
            return False

        cruiseCards = res['cruiseCards']

        for cruiseCard in cruiseCards:
            self.getDetailPage(cruiseCard)

        return True

    def buildCruiseTitle(self, cruiseCard):
        title = str(cruiseCard['duration']) + '-night ' + cruiseCard['destination'] + ' Cruise from ' + cruiseCard[
            'startPort']
        if (cruiseCard['isRoundtrip']):
            title += ' (Roundtrip)'

        return title

    def buildDetailUrl(self, cruiseCard):
        param = {}
        param['cruiseLineCode'] = cruiseCard['cruiseLineCode']
        param['cruiseLineName'] = cruiseCard['cruiseLineName']
        param['shipName'] = cruiseCard['deepLinkShipName']
        param['itineraryId'] = str(cruiseCard['itineraryId'])
        param['duration'] = str(cruiseCard['duration'])
        param['isSponsoredListing'] = str(cruiseCard['sponsoredListing'])
        param['departurePortName'] = cruiseCard['startPort']

        return self.host + 'ItineraryDetails?' + urllib.urlencode(param)

    def getDetailPage(self, cruiseCard):
        url = self.buildDetailUrl(cruiseCard);
        title = self.buildCruiseTitle(cruiseCard);
        req = urllib2.Request(url, headers=self.headers)
        res = json.loads(urllib2.urlopen(req).read())

        if (not (res.has_key('sailingYears'))):
            raise Exception("sailing years lost!")

        data = []
        for sailingYear in res['sailingYears']:
            for sailingMonth in sailingYear['sailingMonths']:
                for sailingDate in sailingMonth['sailingDates']:
                    departureTime = int(sailingDate['departureTimeInMillis'] / 1000)
                    data.append("('travelocity', '" + \
                                str(cruiseCard['itineraryId']) + \
                                "', '" + title + \
                                "', '" + cruiseCard['shipName'] + \
                                "', '" + str(cruiseCard['duration']) + \
                                "', '" + cruiseCard['startPort'] + \
                                "', FROM_UNIXTIME(" + str(departureTime) + \
                                "), '" + str(sailingDate['insideCabinPrice']) + \
                                "', '" + str(sailingDate['oceanViewCabinPrice']) + \
                                "', '" + str(sailingDate['balconyCabinPrice']) + \
                                "', '" + str(sailingDate['suiteCabinPrice']) + \
                                "', '" + str(int(sailingDate['isLowestPrice'])) + \
                                "')")

        db.save(data)
        print title + ' Done! '
