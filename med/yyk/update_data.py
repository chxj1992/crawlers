#!/usr/bin/python
# encoding: utf-8

import sys

from med.yyk import db

reload(sys)
sys.setdefaultencoding('utf8')

sql = 'INSERT INTO doctors_2 (`user_id`, `name`, `title`, `level`, `hospital`, `section`, `photo`, `skills`, `experience`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'

cursor = db.query('SELECT * FROM doctors WHERE 1 ORDER BY `id` ASC', [])

i = 0
while True:
    i += 1
    doctor = cursor.fetchone()
    if doctor is None:
        break

    if i % 1000 == 0:
        print str(i) + ' done'

    title_info = doctor['title'].split(',')
    title, level = '', ''
    if len(title_info) > 0:
        title = title_info[0].strip()
    if len(title_info) > 1:
        level = title_info[1].strip()

    section_info = doctor['section'].split(',')
    section = ''
    if len(title_info) > 0:
        section = section_info[0].strip()

    db.execute(sql, [doctor['user_id'], doctor['name'], title, level, doctor['hospital'], section, doctor['photo'],
                     doctor['skills'], doctor['experience']])
