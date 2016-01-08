import pymongo
import db
from pymongo import MongoClient

client = MongoClient('mongodb://super_admin:super_adminatmedlinker@218.244.136.85:27018/')

figure = client.figure

def saveUser():
    users = figure.user
    userArr = []
    customArr = []
    socialArr = []

    platform = {"sina": '1', "qq": '2'}

    for row in users.find({'type': {'$in': ['sina', 'qq']}}) :

        user = []
        user.append("'"+str(row['id'])+"'")
        user.append("'"+row['uid']+'@platform_'+platform[row['type']]+'.com\'')
        user.append('\'rYclY0UuLFxDfkROOi9R0ugPbXXtfeyhfGaF+RHo9b9GC84UtX6+mehzxsQ5CMrbzAfcNyi+SZMKnFy/29i9ug==\'')
        user.append('\'g4foyl7du5ck0gkwkc8kc440kckk8oo\'')
        user.append('\'ROLE_USER\'')
        user.append("'"+row['name']+"'")
        user.append("'"+str(row['insertTime'])+"'")
        user.append("'"+row['name']+"'")
        user.append("'"+str(1)+"'")

        custom = []
        custom.append("'"+str(row['id'])+"'")
        custom.append("'"+row['avatar']+"'")
        custom.append("''")

        social = []
        social.append("'"+str(row['uid'])+"'")
        social.append("'"+platform[row['type']]+"'")
        social.append("'"+str(row['id'])+"'")

        userStr = ' ,'.join(user)
        userArr.append('('+userStr+')')

        customStr = ' ,'.join(custom)
        customArr.append('('+customStr+')')

        socialStr = ' ,'.join(social)
        socialArr.append('('+socialStr+')')

    db.saveUser(userArr)
    db.saveCustom(customArr)
    db.saveSocial(socialArr)


def saveNews():
    newslist = figure.casem
    newsArr = []

    for row in newslist.find() :
        news = []
        news.append("'"+str(row['id'])+"'")
        news.append("'"+str(row['userId'])+"'")
        news.append("'"+row['pictures'][0]['url']+"'")
        news.append("'"+row['pictures'][0]['desc']+"'")
        news.append("'"+str(row['upCount'])+"'")
        news.append("'0'")
        news.append("FROM_UNIXTIME("+str(row['insertTime'])+")")

        newsStr = ' ,'.join(news)
        newsArr.append('('+newsStr+')')

    db.saveNews(newsArr)


def saveComment():
    commentlist = figure.comment
    commentArr = []
    for row in commentlist.find() :
        comment = []
        comment.append("'"+str(row['casemId'])+"'")
        comment.append("'"+str(row['userId'])+"'")
        comment.append("'0'")
        comment.append("'"+row['text']+"'")
        comment.append("FROM_UNIXTIME("+str(row['insertTime'])+")")

        commentStr = ' ,'.join(comment)
        commentArr = []
        commentArr.append('('+commentStr+')')
        db.saveComment(commentArr)


saveNews()
