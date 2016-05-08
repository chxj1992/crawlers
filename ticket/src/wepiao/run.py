# coding=utf-8
from multiprocessing import Process
from crawler import order_without_area

cookie = 'YII_CSRF_TOKEN=abc37742d27467d5a0d437d4ef8f930d4269e1cb; cid_a1=10015925560998303; cid_1=14569213092998589; x-form=; WEPIAOTOKEN=69a70534ed0afda37c123715dcf175ba; _gat=1; WEPIAO=vg64pjcq48vif1odqp5otlcv55; onlineId=c75868491b564bd49b2bdb8e513d67be; _ga=GA1.2.1046576095.1462440033'
phone = '15669207848'
address = '华西坝大学路12号'
name = '陈先生'
ticket_number = 2
show_id = '14569213092998589'
online_id = '780aa9a6ec0a489bb0e78588cb6d5cbd'

for i in range(1, 11):
    print 'worker ' + str(i) + ' start ...'
    p = Process(target=order_without_area, args=(cookie, show_id, online_id, phone, address, name, ticket_number))
    p.start()
