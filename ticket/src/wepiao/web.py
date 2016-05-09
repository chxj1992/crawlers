# coding=utf-8
import sys
from flask import Flask, request

import crawler

app = Flask(__name__)

default_cookie = cookie = open(sys.path[0] + "/cookie.txt").read().strip()
default_phone = '15669207848'
default_address = '华西坝大学路12号'
default_name = '陈先生'
default_ticket_number = 2


def get_values():
    cookie = request.args.get('cookie', default_cookie)
    phone = request.args.get('phone', default_phone)
    address = request.args.get('address', default_address)
    name = request.args.get('name', default_name)
    ticket_number = request.args.get('ticket_number', default_ticket_number)

    return cookie, phone, address, name, ticket_number


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/with-seats")
def order_with_seats():
    show_id = request.args.get('show_id', '10015925560998303')
    online_id = request.args.get('online_id', 'c75868491b564bd49b2bdb8e513d67be')
    area_id = request.args.get('area_id', '10056561761863882')
    values = get_values()

    return crawler.order_with_seats(values[0], show_id, online_id, area_id, values[1], values[2], values[3], values[4])


@app.route("/without-seats")
def order_without_seats():
    show_id = request.args.get('show_id', '14569213092998589')
    online_id = request.args.get('online_id', '780aa9a6ec0a489bb0e78588cb6d5cbd')
    values = get_values()

    return crawler.order_without_seats(values[0], show_id, online_id, values[1], values[2], values[3], values[4])


if __name__ == "__main__":
    app.run(host='0.0.0.0')
