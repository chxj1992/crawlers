#!/usr/bin/python
# encoding: utf-8

import sys

from med.thread import MyThread
from med.yyk.doctor_list_parser import DoctorListParser

reload(sys)
sys.setdefaultencoding('utf8')

ThreadNum = 1

threads = []

parser = DoctorListParser()

for i in range(1, ThreadNum + 1):
    thread = MyThread(i, parser, ThreadNum, 'get_list')
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()
