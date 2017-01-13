#!/usr/bin/python
# encoding: utf-8

import sys

from med.yyk import db
from med.yyk.doctor_list_parser import DoctorListParser

reload(sys)
sys.setdefaultencoding('utf8')

parser = DoctorListParser()

cursor = db.query('SELECT * FROM doctors WHERE skills is NULL', [])
while True:
    doctor = cursor.fetchone()
    if doctor is None:
        break
    parser.get_detail(str(doctor['user_id']))
