# encoding=utf-8

import json
import re
import time
import requests

import db

class Crawl:
    def __init__(self):
        self.host = "https://disneycruise.disney.go.com/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
            'Accept': 'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'utf-8,gbk;q=0.7,*;q=0.3',
            'Connection': 'close',
            'Content-Type': 'application/json',
            'Authorization': 'BEARER ugH_oCuHbY1JlXTEiQAWYA',
            'Referer': self.host
        }

    def get_token(self):        
        url = self.host + 'wam/authentication/get-client-token/'
        res = requests.get(url)
        print res.json()
         

    def run(self):
        payload = {"currency":"USD","affiliations":[],"partyMix":[{"accessible":False,"adultCount":2,"childCount":0,"orderBuilderId":None,"nonAdultAges":[],"partyMixId":"0"}]}
        url = self.host + 'wam/cruise-sales-service/cruise-listing/?region=INTL&storeId=DCL&view=cruise-listing'
        res = requests.post(url, json=payload, headers=self.headers)

        print res.json()
        
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

if __name__ == "__main__":
    c = Crawl()
    c.get_token()


