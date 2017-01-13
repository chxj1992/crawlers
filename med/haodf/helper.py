#!/usr/bin/python
# encoding: utf-8
import requests


def get_http_proxy(counter=0):
    try:
        counter += 1
        url = 'http://crawlers.chxj.name/proxy/hidemyass/shuffle?protocol=http'
        proxy = requests.get(url).json()
        url = 'http://' + proxy['ip'] + ':' + proxy['port']
        print 'proxies: ' + url
        return url
    except Exception as e:
        print 'retry get proxy'
        if counter > 10:
            print 'proxy service is down'
            return False
