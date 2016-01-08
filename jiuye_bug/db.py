import MySQLdb
        

def save(data):
    sql = 'REPLACE INTO user(username, md5, password) VALUES '+','.join(data);  
    execute(sql)


def execute(sql):
    try:
        conn=MySQLdb.connect(host='localhost', user='jiuye', passwd='jiuye', db='jiuye', port=3306)
        cur=conn.cursor()
        res = cur.execute(sql)
        conn.commit();
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


