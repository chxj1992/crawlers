# coding=utf-8
import random
import re

import requests
from bs4 import BeautifulSoup


def shuffle(proxy_list):
    random.shuffle(proxy_list)
    return proxy_list.pop()


def samair():
    return Samair().proxy_list()


def ssl_proxies():
    return SSLProxies().proxy_list()


class Samair:
    def __init__(self):
        self.url = 'http://www.samair.ru'

    def proxy_list(self):
        try:
            content = requests.get(self.url + '/proxy').text
            soup = BeautifulSoup(content, 'lxml')
            proxy_elem_list = soup.find(id='proxylist').find_all('span')
            css_path = soup.find('link').find_next().get('href')

            port_map = self.get_port_map(css_path)
            proxy_list = []
            for proxy_elem in proxy_elem_list:
                proxy_list.append({
                    'ip': proxy_elem.get_text()[0:-1],
                    'port': port_map[proxy_elem.get('class')[0]],
                })

            return proxy_list
        except Exception as e:
            print e.message
            return {'error': 'system error'}

    def get_port_map(self, css_path):
        content = requests.get(self.url + css_path).text
        matches = re.findall('\.(\w+)\:.*\"(\d+)\"', content)
        port_map = {}
        for match in matches:
            port_map[match[0]] = match[1]

        return port_map


class SSLProxies:
    def __init__(self):
        self.url = 'http://www.sslproxies.org/'

    def proxy_list(self):
        try:
            content = requests.get(self.url).text
            soup = BeautifulSoup(content, 'lxml')
            table = soup.find(id='proxylisttable')
            proxy_elem_list = table.find('tbody').find_all('tr')

            return map(lambda proxy_elem:
                       {'ip': proxy_elem.find('td').get_text(),
                        'port': proxy_elem.find('td').find_next().get_text()},
                       proxy_elem_list)
        except Exception as e:
            print e.message
            return {'error': 'system error'}


class HideMyAss:
    def __init__(self):
        self.url = 'http://proxylist.hidemyass.com/'
        self.headers = {
            'X-Requested-With': 'XMLHttpRequest'
        }
        # fuck the GFW, socks proxies option requires `requests>=2.10`
        self.proxies = {
            'http': "socks5://127.0.0.1:1080",
            'https': "socks5://127.0.0.1:1080"
        }

    def proxy_list(self, condition={}, fuck_gfw=False):
        try:
            if not fuck_gfw:
                self.proxies = {}

            res = requests.get(self.url, headers=self.headers, proxies=self.proxies).json()
            soup = BeautifulSoup(res['table'], 'lxml')
            tr = soup.find('tr')
            return self.get_style_map(tr.find('style'))
        except Exception as e:
            print e.message
            return {'error': 'system error'}

    @staticmethod
    def get_style_map(style_elem):
        matches = re.findall('\.(.*)\{(.*)\}', style_elem.get_text())
        style_map = {}
        for match in matches:
            style_map[match[0]] = match[1]

        return style_map


print HideMyAss().proxy_list({}, True)
