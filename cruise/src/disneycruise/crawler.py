# encoding=utf-8

import requests


class Crawler:
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

    def run(self, page):
        payload = {"currency": "USD", "affiliations": [], "partyMix": [
            {"accessible": False, "adultCount": 2, "childCount": 0, "orderBuilderId": None, "nonAdultAges": [],
             "partyMixId": "0"}]}
        url = self.host + 'wam/cruise-sales-service/cruise-listing/?region=INTL&storeId=DCL&view=cruise-listing'
        res = requests.post(url, json=payload, headers=self.headers).json()

        print res
        return False
