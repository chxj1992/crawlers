#!/usr/bin/python
# encoding: utf-8

import sys

from med.haodf_doctor import db
from med.haodf_doctor.doctor_list_parser import DoctorListParser
from med.haodf_doctor.thread import MyThread

reload(sys)
sys.setdefaultencoding('utf8')

parser = DoctorListParser()

ThreadNum = 10

cursor = db.query('SELECT * FROM jibing WHERE  1 ORDER BY `id` ASC', [])

while True:
    jibing = cursor.fetchone()
    if jibing is None:
        break

    print 'jibing : ' + jibing['name']
    threads = []
    for i in range(1, ThreadNum + 1):
        parser = DoctorListParser()
        thread = MyThread(i, parser, ThreadNum, jibing['name'])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
