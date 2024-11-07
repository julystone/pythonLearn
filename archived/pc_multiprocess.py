import os
import random
import time
from multiprocessing import Process, Queue, Manager


def consumer(queue, shared_dict: dict):
    while True:
        res = queue.get()
        time.sleep(random.randint(1, 3))
        print(shared_dict.keys())
        print('\033[43m%s 吃 %s\033[0m' % (os.getpid(), res))


def producer(queue, shared_dict: dict):
    for i in range(10):
        time.sleep(random.randint(1, 3))
        res = '包子%s' % i
        shared_dict.__setitem__(i, i)
        queue.put(res)
        print('\033[44m%s 生产了 %s\033[0m' % (os.getpid(), res))


if __name__ == '__main__':
    q = Queue()
    with Manager() as manager:
        share = manager.dict()
        print(share)
        # 生产者们:即厨师们
        p1 = Process(target=producer, args=(q, share))

        # 消费者们:即吃货们
        c1 = Process(target=consumer, args=(q, share))

    # 开始
    p1.start()
    c1.start()
    print('主')
