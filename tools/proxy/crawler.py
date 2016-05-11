# coding=utf-8
import json
import random
import re

import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://www.samair.ru'


def shuffle():
    try:
        proxy_list = Crawler().get_proxy_list()
        random.shuffle(proxy_list)
        return json.dumps(proxy_list.pop())
    except Exception as e:
        print e.message
        return 'system error'


class Crawler:
    def __init__(self):
        pass

    def get_proxy_list(self):
        content = requests.get(BASE_URL + '/proxy').text
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

    @staticmethod
    def get_port_map(css_path):
        content = requests.get(BASE_URL + css_path).text
        matches = re.findall('\.(\w+)\:.*\"(\d+)\"', content)

        port_map = {}
        for match in matches:
            port_map[match[0]] = match[1]

        return port_map
