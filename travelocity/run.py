import crawl
import urllib2
from multiprocessing import Process
import os

WORKER_NUM = 20

c = crawl.Crawl()

def worker(i, step): 
    print( "worker : " + str(i) + " start ...")
    while True :
        try:
            if (c.getListPage(i) == False) :
                break
        except :
            print("url error caught!")
            continue
        i += step
        print 'page ' + str(i)
    print( "worker : " + str(i) + " end.")


for i in range(0, WORKER_NUM):
    p = Process(target = worker, args = (i, WORKER_NUM,))
    p.start()

