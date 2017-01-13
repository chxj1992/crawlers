#!/usr/bin/python
# encoding: utf-8

import threading


class MyThread(threading.Thread):
    def __init__(self, thread_id, parser, thread_num, method_name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.parser = parser
        self.thread_num = thread_num
        try:
            self.method = getattr(self.parser, method_name)
        except AttributeError:
            raise NotImplementedError(
                    "Class `{}` does not implement `{}`".format(self.parser.__class__.__name__, method_name))

    def run(self):
        print "Starting thread " + str(self.thread_id)
        page = self.thread_id

        while self.method(page):
            print "page : " + str(page)
            page += self.thread_num
        print "Exiting thread " + str(self.thread_id)
