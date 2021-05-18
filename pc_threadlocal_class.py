# -*- coding: utf-8 -*-
# @File   :   __init__.py.py
# @Author :   julystone
# @Date   :   2020/12/4 16:06
# @Email  :   july401@qq.com
import threading

global_data = threading.local()


def show():
    print(threading.current_thread().getName(), global_data.hh.july)


class HappyLearn:
    july = 111

    @classmethod
    def setJuly(cls, handsome):
        cls.july = handsome

    @classmethod
    def getJuly(cls):
        return cls.july

    @staticmethod
    def printJuly():
        print(HappyLearn.july)


def thread_cal():
    global_data.hh = HappyLearn()
    for _ in range(1000):
        global_data.hh.july = _
    show()


happy1 = HappyLearn()
print(happy1.july)
threads = []
for i in range(10):
    threads.append(threading.Thread(target=thread_cal))
    threads[i].start()

print(global_data)
print("Main thread: ", global_data.__dict__)  # {}

print(happy1.july)
