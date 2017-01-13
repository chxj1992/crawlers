# -*- coding: utf-8 -*-

import pymysql.cursors


def save_url(url):
    sql = 'INSERT INTO pages(`url`) VALUES (%s)'
    execute(sql, [url])


def get_url(url):
    sql = 'SELECT * FROM pages WHERE `url`=%s'
    return query(sql, [url])


def query(sql, data):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            return cursor.fetchone()
    finally:
        connection.close()


def execute(sql, data):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, data)
        connection.commit()
    finally:
        connection.close()


def connect():
    return pymysql.connect(host='127.0.0.1',
                           user='root',
                           password='87822971',
                           db='inquiry',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
