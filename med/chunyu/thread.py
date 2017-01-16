#!/usr/bin/python
# encoding: utf-8

import threading


class MyThread(threading.Thread):
    def __init__(self, thread_id, parser, thread_num, section_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.parser = parser
        self.thread_num = thread_num
        self.section_id = section_id

    def run(self):
        print "Starting thread " + str(self.thread_id)
        page = self.thread_id

        while self.parser.get_list(self.section_id, page):
            print "page : " + str(page)
            page += self.thread_num
        print "Exiting thread " + str(self.thread_id)
