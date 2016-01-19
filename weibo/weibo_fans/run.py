#encoding=utf-8
from crawl import Crawl


useridFile = open("userid.txt", 'r')
userid = useridFile.read().strip()
useridFile.close()

open("result.txt", 'w').close()

c = Crawl()

print "Job Started ...\n"
page = 1
url = c.host + '/'+userid+'/myfans?t=4&page=' + str(page)
while ( c.run(url) ):
    print "fans in page "+str(page)+"\n"
    page += 1 
    url = c.host + '/'+userid+'/myfans?t=4&page=' + str(page)

print "Done!\n"
