import MySQLdb

def save(data):
    sql = 'REPLACE INTO itineraries(itinerary_id, title, ship_name, duration, departure_port, departure_time, \
            inside, oceanview, balcony, suite, is_lowest_price) VALUES ' + ','.join(data);  
    execute(sql)

def execute(sql):
    try:
        conn=MySQLdb.connect(host='localhost', user='root', passwd='87822971', db='travelocity', port=3306)
        cur=conn.cursor()
        res = cur.execute(sql)
        conn.commit();
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


