# coding=utf-8
import sys

from flask import request, Module

from ticket.wepiao import crawler

wepiao = Module(__name__, 'wepiao')

default_cookie = open(sys.path[0] + "/web/ticket/wepiao/cookie.txt").read().strip()
default_phone = '15528285053'
default_address = '天府软件园D6座7层'
default_name = '陈晓敬'
default_ticket_number = 2


def get_values():
    cookie = request.args.get('cookie', default_cookie)
    phone = request.args.get('phone', default_phone)
    address = request.args.get('address', default_address)
    name = request.args.get('name', default_name)
    ticket_number = request.args.get('ticket_number', default_ticket_number)

    return cookie, phone, address, name, ticket_number


@wepiao.route("/wepiao/with-seats")
def order_with_seats():
    online_id = request.args.get('online_id', 'c75868491b564bd49b2bdb8e513d67be')
    area_id = request.args.get('area_id', '10056561761863882')
    values = get_values()

    return crawler.order_with_seats(values[0], online_id, area_id, values[1], values[2], values[3], values[4])


@wepiao.route("/wepiao/without-seats")
def order_without_seats():
    online_id = request.args.get('online_id', '780aa9a6ec0a489bb0e78588cb6d5cbd')
    values = get_values()

    return crawler.order_without_seats(values[0], online_id, values[1], values[2], values[3], values[4])
