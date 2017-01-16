#!/usr/bin/python
# encoding: utf-8

import sys

from med.chunyu.doctor_list_parser import DoctorListParser
from med.chunyu.thread import MyThread

reload(sys)
sys.setdefaultencoding('utf8')

ThreadNum = 10

threads = []

parser = DoctorListParser()

for section_id in range(1, 17 + 1):
    print 'section id ' + str(section_id)
    for i in range(1, ThreadNum + 1):
        thread = MyThread(i, parser, ThreadNum, section_id)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    threads = []
