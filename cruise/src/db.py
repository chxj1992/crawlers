# -*- coding: utf-8 -*-
import os

import MySQLdb


def save(data):
    sql = 'REPLACE INTO cruises(project, itinerary_id, title, ship_name, duration, departure_port, departure_time, \
            inside, oceanview, balcony, suite, is_lowest_price) VALUES ' + ','.join(data)
    execute(sql)


def execute(sql):
    host = os.environ.get("DB_HOST")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASS")
    port = int(os.environ.get("DB_PORT"))
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=password, db='apples_data_center', port=port,
                               use_unicode=True, charset="utf8")
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
