#!/usr/bin/python
# encoding: utf-8

import sys

from med.chunyu import db
from med.chunyu.doctor_list_parser import DoctorListParser

reload(sys)
sys.setdefaultencoding('utf8')

parser = DoctorListParser()

while True:
    cursor = db.query('SELECT * FROM doctors WHERE intro is NULL', [])
    while True:
        doctor = cursor.fetchone()
        if doctor is None:
            break
        parser.get_detail(str(doctor['user_id']))
