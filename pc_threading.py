import os
import queue
import random
import time
from threading import Thread, Lock


class DisPatcher:
    def __init__(self):
        self.lock = Lock()
        self.queue = queue.Queue()
        self.d = {}

    def consumer(self):
        while True:
            with self.lock:
                print(self.d)
            res = self.queue.get()
            time.sleep(random.randint(1, 3))
            print('\033[43m%s 吃 %s\033[0m' % (os.getpid(), res))

    def producer(self):
        for i in range(10):
            time.sleep(random.randint(1, 3))
            res = '包子%s' % i
            with self.lock:
                self.d.__setitem__(i, i)
            self.queue.put(res)
            print('\033[44m%s 生产了 %s\033[0m' % (os.getpid(), res))


if __name__ == '__main__':
    # 生产者们:即厨师们
    d = DisPatcher()
    p1 = Thread(target=d.producer, args=())

    # 消费者们:即吃货们
    c1 = Thread(target=d.consumer, args=())

    # 开始
    p1.start()
    c1.start()
    c1.join()
    print('主')
