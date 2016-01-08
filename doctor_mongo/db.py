import MySQLdb

def saveUser(data):
    sql = 'REPLACE INTO users(id, email, password, salt, roles, name, time_created, username, isEnabled) VALUES '+','.join(data);  
    execute(sql)


def saveCustom(data):
    sql = 'REPLACE INTO user_real_custom_fields(user_id, avatar, location) VALUES '+','.join(data);  
    execute(sql)


def saveSocial(data):
    sql = 'REPLACE INTO social_users(open_id, platform, user_id) VALUES '+','.join(data);  
    execute(sql)


def saveNews(data):
    sql = 'REPLACE INTO news(id, user_id, image, content, heat, channel_id, createtime) VALUES '+','.join(data);  
    execute(sql)


def saveComment(data):
    print data
    sql = 'REPLACE INTO comment(news_id, user_id, to_comment_id, content, createtime) VALUES '+','.join(data);  
    print sql
    execute(sql)


def execute(sql):
    try:
        conn=MySQLdb.connect(host='localhost', user='root', passwd='87822971', db='test', port=3306, charset="utf8")
        cur=conn.cursor()
        res = cur.execute(sql)
        conn.commit();
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


