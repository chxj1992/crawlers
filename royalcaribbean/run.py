from multiprocessing import Process

import crawl

WORKER_NUM = 20
RETRY_MAX = 10

c = crawl.Crawl()


def worker(i, step):
    print("worker : " + str(i) + " start ...")
    retry = 0
    while True:
        try:
            if not c.getListPage(i):
                break
        except:
            print("url error caught!")
            retry += 1
            if retry < RETRY_MAX:
                print 'retry : ' + str(retry)
                continue
        i += step
        retry = 0
        print 'page ' + str(i)
    print("worker : " + str(i) + " end.")
    return True


if __name__ == "__main__":
    for i in range(0, WORKER_NUM):
        p = Process(target=worker, args=(i, WORKER_NUM,))
        p.start()
