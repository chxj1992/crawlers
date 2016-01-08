import MySQLdb
import json

def execute(sql, data):
    db=MySQLdb.connect(host='localhost', user='root', passwd='87822971', db='weibo', port=3306)
    cursor = db.cursor() 
    cursor.executemany(sql, data)
    db.commit();
    cursor.close()
    db.close()

