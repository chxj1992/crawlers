# encoding=utf-8
# -*- coding: utf-8 -*-

import getopt
import importlib

import sys

from multiprocessing import Process


def usage():
    print '==========================================='
    print 'example: python run.py -p travelocity -n 10\n'
    print '--help (-h) : show help'
    print '--project (-p) : project name'
    print '--number (-n) : worker number'
    print '==========================================='
    sys.exit(2)


opts = []

try:
    opts, args = getopt.getopt(sys.argv[1:], 'n:p:h', ['number=', 'project=', 'help'])
except getopt.GetoptError as e:
    print 'error: ' + str(e)
    usage()

worker_number = 1
project = 'travelocity'

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
    elif opt in ('-n', '--number'):
        worker_number = int(arg)
    elif opt in ('-p', '--project'):
        project = str(arg)
    else:
        usage()

m = importlib.import_module('src.' + project + '.crawler')
c = m.Crawler()


def worker(i, step):
    print("worker : " + str(i) + " start ...")
    page = i
    while True:
        try:
            if not c.run(page):
                break
        except Exception as e:
            print "error : " + str(e)
            continue
        print 'page : ' + str(page) + " finished"
        page += step
    print("worker : " + str(i) + " end.")
    return True


if __name__ == "__main__":
    for i in range(0, worker_number):
        p = Process(target=worker, args=(i + 1, worker_number,))
        p.start()
