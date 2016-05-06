# coding=utf-8
from flask import Flask

import crawler

app = Flask(__name__)

cookie = 'YII_CSRF_TOKEN=abc37742d27467d5a0d437d4ef8f930d4269e1cb; cid_a1=10015925560998303; WEPIAOTOKEN=269ccb25fa4da0631c2a6312a913f606; WEPIAO=f1goahkju01jdtggo0gp3ci3a0; cid_1=14569213092998589; x-form=; onlineId=780aa9a6ec0a489bb0e78588cb6d5cbd; _gat=1; _ga=GA1.2.1046576095.1462440033'
phone = '15669207848'
address = '华西坝大学路12号'
name = '陈先生'
ticket_number = 2


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/with-area")
def order_with_area():
    show_id = '10015925560998303'
    online_id = 'c75868491b564bd49b2bdb8e513d67be'
    area_id = '10056561761863882'
    return crawler.order_with_area(cookie, show_id, online_id, area_id, phone, address, name, ticket_number)


@app.route("/without-area")
def order_without_area():
    show_id = '14569213092998589'
    online_id = '780aa9a6ec0a489bb0e78588cb6d5cbd'
    return crawler.order_without_area(cookie, show_id, online_id, phone, address, name, ticket_number)


if __name__ == "__main__":
    app.run()
