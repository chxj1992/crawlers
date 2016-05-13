# coding=utf-8
from multiprocessing import Process

import sys

from crawler import order_without_seats

cookie = open(sys.path[0] + "/cookie.txt").read().strip()
phone = '15528285053'
address = '天府软件园D6座7层'
name = '陈晓敬'
ticket_number = 2
online_id = 'eedef99067d24943a022d04f19781a95'

for i in range(1, 11):
    print 'worker ' + str(i) + ' start ...'
    p = Process(target=order_without_seats, args=(cookie, online_id, phone, address, name, ticket_number))
    p.start()
