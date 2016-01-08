import MySQLdb

def saveOffenceRate(data):
    sql = 'REPLACE INTO data_offence_rate(school_name, data_time, rate) VALUES '+','.join(data);  
    execute(sql)


def execute(sql):
    try:
        conn=MySQLdb.connect(host='localhost', user='root', passwd='87822971', db='driving_school', port=3306)
        cur=conn.cursor()
        res = cur.execute(sql)
        conn.commit();
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


