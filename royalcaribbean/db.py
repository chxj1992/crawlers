import MySQLdb


def save(data):
    sql = 'REPLACE INTO cruises(`from`, itinerary_id, title, ship_name, duration, departure_port, departure_time, \
            inside, oceanview, balcony, suite) VALUES ' + ','.join(data)
    execute(sql)


def execute(sql):
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='87822971', db='apples_data_center', port=3306)
        cur = conn.cursor()
        res = cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
