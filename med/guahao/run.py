#!/usr/bin/python
# encoding: utf-8

import sys

from med.guahao import db
from med.guahao.doctor_list_parser import DoctorListParser
from med.guahao.thread import MyThread

reload(sys)
sys.setdefaultencoding('utf8')

ThreadNum = 10

threads = []

parser = DoctorListParser()

hospital_cursor = db.query('SELECT * FROM hospitals WHERE 1', [])
while True:
    hospital = hospital_cursor.fetchone()
    if hospital is None:
        break
    section_cursor = db.query('SELECT * FROM sections WHERE 1', [])
    while True:
        section = section_cursor.fetchone()
        if section is None:
            break

        print 'hospital ' + hospital['name'] + ' id ' + hospital['key']
        print 'section ' + section['name'] + ' id ' + section['key']

        for i in range(1, ThreadNum + 1):
            thread = MyThread(i, parser, ThreadNum, section['key'], hospital['key'])
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        threads = []
