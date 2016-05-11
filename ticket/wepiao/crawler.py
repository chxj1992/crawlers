# coding=utf-8
import json
import random
import re

import requests


def order_with_seats(cookie, show_id, online_id, area_id, phone, address, name, num):
    try:
        c = Crawler(cookie, show_id, online_id, area_id)

        # 选座
        map(lambda seat: c.mt_seat(seat['seatId']), c.get_seats(num))
        # 下单
        c.create_order(phone, address, name)
        return 'success!'
    except Exception as e:
        return 'failed!'


def order_without_seats(cookie, show_id, online_id, phone, address, name, num):
    try:
        c = Crawler(cookie, show_id, online_id)

        # 订票
        c.add_tickets(num)
        # 下单
        c.create_order(phone, address, name)
        return 'success!'
    except Exception as e:
        return 'failed!'


SEAT_STATUS_AVAILABLE = 1


class Crawler:
    def __init__(self, cookie, show_id, online_id, area_id=''):
        self.show_id = show_id
        self.online_id = online_id
        self.area_id = area_id
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
            'Cookie': cookie,
        }

    def get_seats(self, n=1):
        url = 'http://www.wepiao.com/index.php?r=item/seats&onlineId=' + self.online_id + '&showId=' + self.show_id + '&areaId=' + self.area_id

        res = requests.get(url=url, headers=self.header).text
        matches = re.search('\[\{.*\}\]', res)
        seats = json.loads(matches.group(0))
        available_seats = filter(lambda seat: seat['seatStatus'] == SEAT_STATUS_AVAILABLE, seats)

        start = random.randint(0, len(available_seats) - n)
        return available_seats[start:start + n]

    def mt_seat(self, seat_id):
        url = 'http://www.wepiao.com/index.php?r=cart/MTSeat'

        data = {
            'onlineId': self.online_id,
            'showId': self.show_id,
            'areaId': self.area_id,
            'chooseSeatId': seat_id,
        }

        res = requests.post(url=url, data=data, headers=self.header).json()
        print res

    def add_tickets(self, n=1):
        url = 'http://www.wepiao.com/index.php?r=cart/addTickets'
        data = {
            'tickets[' + self.get_price_id() + ']': n,
            'onlineId': self.online_id,
            'showId': self.show_id,
        }
        res = requests.post(url=url, data=data, headers=self.header)
        res.encoding = 'UTF-8'

    def get_price_id(self):
        url = 'http://www.wepiao.com/index.php?r=item/ajaxPrices'
        data = {
            'screeningId': self.get_screen_id(),
            'onlineId': self.online_id
        }
        res = requests.post(url=url, data=data, headers=self.header).json()
        available_prices = filter(lambda price: price['stockNum'] > 10, res['prices'])

        return available_prices[0]['priceId']

    def get_screen_id(self):
        url = 'http://www.wepiao.com/index.php?r=item/detail/id/' + self.online_id
        res = requests.get(url=url, headers=self.header).text
        matches = re.search('class=\"screening\".*id=\"(\d+)\"', res)
        return matches.group(1)

    def create_order(self, phone, address, name):
        url = 'http://www.wepiao.com/index.php?r=order/create'

        data = {
            'deliveryMethod': '3',
            'paypaymentType': '1',
            'provinceId': '23',
            'cityId': '235',
            'districtId': '2043',
            'buyUserMobile': phone,
            'deliveryAddress': address,
            'receiveDeliveryPerson': name,
            'receiveDeliveryMobile': phone,
            'same-to-phone': 'on',
            'payWay': 'wechat',
        }

        res = requests.post(url=url, data=data, headers=self.header)
        res.encoding = 'UTF-8'
        if re.search(u'订单', res.text):
            print 'success!'
        else:
            print 'failed!'
            raise Exception('failed!')
