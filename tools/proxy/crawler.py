# coding=utf-8
import random
import re

import requests
from bs4 import BeautifulSoup


def shuffle(proxy_list):
    try:
        random.shuffle(proxy_list)
        return proxy_list.pop()
    except Exception as e:
        return {'error': 'system error', 'msg': e.message}


def samair():
    return Samair().proxy_list()


def ssl_proxies():
    return SSLProxies().proxy_list()


def hide_my_ass(protocol):
    return HideMyAss().proxy_list(protocol, True)


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
                    'protocol': 'http',
                })

            return proxy_list
        except Exception as e:
            print e.message
            return {'error': 'system error', 'msg': e.message}

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
                       {
                           'ip': proxy_elem.find('td').get_text(),
                           'port': proxy_elem.find('td').find_next().get_text(),
                           'protocol': 'https',

                       },
                       proxy_elem_list)
        except Exception as e:
            print e.message
            return {'error': 'system error', 'msg': e.message}


class HideMyAss:
    def __init__(self):
        self.url = 'http://proxylist.hidemyass.com/'
        self.headers = {
            'X-Requested-With': 'XMLHttpRequest',
        }
        # fuck the GFW, socks proxies option requires `requests>=2.10`
        self.proxies = {
            'http': "socks5://127.0.0.1:1080",
            'https': "socks5://127.0.0.1:1080"
        }

    def proxy_list(self, protocol='http', fuck_gfw=False):
        try:
            if not fuck_gfw:
                self.proxies = {}

            res = requests.post(self.url, headers=self.headers, proxies=self.proxies).json()
            soup = BeautifulSoup(res['table'], 'lxml')

            proxy_list = []
            for row in soup.find_all('tr'):
                regexp = self.build_hidden_reg_exp(row.find('style'))
                clean_row = re.sub(regexp, '', str(row))
                row_soup = BeautifulSoup(clean_row, 'lxml')
                matches = re.match('.*?(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s+(\w+)\s+(\S+)', row_soup.get_text())
                p = matches.group(4).lower()
                if p == protocol:
                    proxy_list.append({
                        'ip': matches.group(1),
                        'port': matches.group(2),
                        'protocol': p,
                    })
            return proxy_list
        except Exception as e:
            print e.message
            return {'error': 'system error', 'msg': e.message}

    def build_hidden_reg_exp(self, style_elem):
        regexp = '<style>[\s\S]*?<\/style>|<\w+ style="display:none.*?>.*?<\/.*?>'
        style_map = self.get_style_map(style_elem)
        for style in style_map:
            if style_map[style] == 'display:none':
                regexp += '|<\w+ class="' + style + '">.*?<\/.*?>'
        return regexp

    @staticmethod
    def get_style_map(style_elem):
        matches = re.findall('\.(.*)\{(.*)\}', style_elem.get_text())
        style_map = {}
        for match in matches:
            style_map[match[0]] = match[1]

        return style_map
