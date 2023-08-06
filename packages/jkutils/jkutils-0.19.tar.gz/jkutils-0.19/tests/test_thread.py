# -*-coding:utf-8-*-

"""
@author: teddy
@file: test_thread.py
@time: 2020/4/12 10:55 AM
@description:
"""
import time
from threading import Thread, Timer


class Worker(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        # while True:
        time.sleep(int(self.name))
        print(f"[run]:{self.name}")


def time_func(i):
    print(f"[time_func]:{i}")


if __name__ == "__main__":
    # for i in range(2):
    #     w = Worker(i)
    #     if i % 2 == 0:
    #         print(i)
    #         w.daemon = True
    #     w.start()
    w1 = Worker(1)
    w2 = Worker(5)
    # w2.daemon = True
    w1.start()
    w2.start()
    t = Timer(10, time_func, [1,])
    t.start()
    index = 0
    while True:
        print(index)
        time.sleep(1)
        index += 1
