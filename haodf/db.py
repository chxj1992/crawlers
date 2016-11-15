# -*- coding: utf-8 -*-

import pymysql.cursors


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
