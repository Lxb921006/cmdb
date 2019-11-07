#!/usr/bin/env python3
# coding   : utf-8
# @Time    : 2019/8/1 0001 10:32
# @Author  : lxb
# @FileName: t_queue.py
# @Software: PyCharm
# @Desc    : The role of the script

import time
import threading
import random
from queue import Queue


class test(threading.Thread):

    def __init__(self, q):
        self.q = q
        super().__init__()

    def run(self):
        while 1:
            data = self.q.get()
            self.mission(data)
            if self.q.task_done():
                break
            time.sleep(random.randrange(2, 5))

    def mission(self, data):
        print(data)


if __name__ == '__main__':
    q = Queue()
    for i in range(100):
        q.put(i)

    for _ in range(10):
        t = test(q)
        t.daemon = True
        t.start()

    q.join()






