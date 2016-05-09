# coding=utf-8
from multiprocessing import Process

import sys

from crawler import order_without_seats

cookie = open(sys.path[0] + "/cookie.txt").read().strip()
phone = '15669207848'
address = '华西坝大学路12号'
name = '陈先生'
ticket_number = 2
show_id = '14569213092998589'
online_id = '780aa9a6ec0a489bb0e78588cb6d5cbd'

for i in range(1, 11):
    print 'worker ' + str(i) + ' start ...'
    p = Process(target=order_without_seats, args=(cookie, show_id, online_id, phone, address, name, ticket_number))
    p.start()
