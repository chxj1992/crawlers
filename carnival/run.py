# encoding=utf-8

from multiprocessing import Process

import crawl

WORKER_NUM = 2

c = crawl.Crawl()


def worker(i, step):
    print("worker : " + str(i) + " start ...")
    page = i + 1
    while True:
        try:
            if not c.getListPage(page):
                break
        except Exception as e:
            print "error : " + str(e)
            continue
        print 'page : ' + str(page)
        page += step
    print("worker : " + str(i) + " end.")
    return True


if __name__ == "__main__":
    for i in range(0, WORKER_NUM):
        p = Process(target=worker, args=(i, WORKER_NUM,))
        p.start()
