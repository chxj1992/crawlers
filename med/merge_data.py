#!/usr/bin/python
# encoding: utf-8
import hashlib
import sys

from med import db
from med.baikemy import db as baikemy_db
from med.chunyu import db as chunyu_db
from med.guahao import db as guahao_db
from med.haodf_doctor import db as haodf_db
from med.myzd import db as myzd_db
from med.yyk import db as yyk_db


def get_hash(name, hospital, section):
    return hashlib.md5(
            u' '.join((name.strip(), hospital.strip(), section.strip())
                      ).encode('utf-8').strip()).hexdigest()


sql = 'INSERT INTO doctors (`user_hash`, `name`, `title`, `level`, `hospital`, `section`, `photo`, `skills`, `experience`, `workplace`, `source`, `source_user_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'


# 好大夫
def haodf():
    cursor = haodf_db.query('SELECT * FROM doctors WHERE 1 ORDER BY `id` ASC', [])
    i = 0
    while True:
        i += 1
        doctor = cursor.fetchone()
        if doctor is None:
            break

        if i % 1000 == 0:
            print str(i) + ' done'

        user_hash = get_hash(doctor['name'], doctor['hospital'], doctor['section'])
        try:
            db.execute(sql,
                       [user_hash, doctor['name'], doctor['title'], doctor['level'], doctor['hospital'],
                        doctor['section'], doctor['photo'], doctor['skills'], doctor['experience'], '',
                        'haodf', doctor['user_id']])
        except Exception:
            print user_hash + ' ' + str(sys.exc_info())


# 名医百科
def baikemy():
    cursor = baikemy_db.query('SELECT * FROM doctors WHERE 1 ORDER BY `id` ASC', [])
    i = 0
    while True:
        i += 1
        doctor = cursor.fetchone()
        if doctor is None:
            break

        if i % 1000 == 0:
            print str(i) + ' done'

        user_hash = get_hash(doctor['name'], doctor['hospital'], doctor['section'])
        try:
            db.execute(sql,
                       [user_hash, doctor['name'], doctor['title'], '', doctor['hospital'],
                        doctor['section'], doctor['photo'], doctor['skills'], doctor['experience'], '',
                        'baikemy', doctor['user_id']])
        except Exception:
            print user_hash + ' ' + str(sys.exc_info())


# 春雨医生
def chunyu():
    cursor = chunyu_db.query('SELECT * FROM doctors WHERE 1 ORDER BY `id` ASC', [])
    i = 0
    while True:
        i += 1
        doctor = cursor.fetchone()
        if doctor is None:
            break

        if i % 1000 == 0:
            print str(i) + ' done'

        user_hash = get_hash(doctor['name'], doctor['hospital'], doctor['section'])
        try:
            db.execute(sql,
                       [user_hash, doctor['name'], doctor['title'], '', doctor['hospital'],
                        doctor['section'], doctor['photo'], doctor['skills'], doctor['intro'], doctor['workplace'],
                        'chunyu', doctor['user_id']])
        except Exception:
            print user_hash + ' ' + str(sys.exc_info())


# 名医主刀
def myzd():
    cursor = myzd_db.query('SELECT * FROM doctors WHERE 1 ORDER BY `id` ASC', [])
    i = 0
    while True:
        i += 1
        doctor = cursor.fetchone()
        if doctor is None:
            break

        if i % 1000 == 0:
            print str(i) + ' done'

        user_hash = get_hash(doctor['name'], doctor['hospital'], doctor['section'])
        try:
            db.execute(sql,
                       [user_hash, doctor['name'], doctor['title'], doctor['level'], doctor['hospital'],
                        doctor['section'], doctor['photo'], doctor['skills'], doctor['experience'], '',
                        'myzd', doctor['user_id']])
        except Exception:
            print user_hash + ' ' + str(sys.exc_info())


# 微医
def guahao():
    cursor = guahao_db.query('SELECT * FROM doctors WHERE 1 ORDER BY `id` ASC', [])
    i = 0
    while True:
        i += 1
        doctor = cursor.fetchone()
        if doctor is None:
            break

        if i % 1000 == 0:
            print str(i) + ' done'

        user_hash = get_hash(doctor['name'], doctor['hospital'], doctor['section'])
        try:
            db.execute(sql,
                       [user_hash, doctor['name'], doctor['title'], doctor['level'], doctor['hospital'],
                        doctor['section'], doctor['photo'], doctor['skills'], doctor['intro'], '',
                        'guahao', doctor['user_id']])
        except Exception:
            print user_hash + ' ' + str(sys.exc_info())


# 39就医助手
def yyk():
    cursor = yyk_db.query('SELECT * FROM doctors_2 WHERE 1 ORDER BY `id` ASC', [])
    i = 0
    while True:
        i += 1
        doctor = cursor.fetchone()
        if doctor is None:
            break

        if i % 1000 == 0:
            print str(i) + ' done'

        user_hash = get_hash(doctor['name'], doctor['hospital'], doctor['section'])
        try:
            db.execute(sql,
                       [user_hash, doctor['name'], doctor['title'], doctor['level'], doctor['hospital'],
                        doctor['section'], doctor['photo'], doctor['skills'], doctor['experience'], '',
                        'yyk', doctor['user_id']])
        except Exception:
            print user_hash + ' ' + str(sys.exc_info())


haodf()
