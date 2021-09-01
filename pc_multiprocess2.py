import os
import random
import time
from multiprocessing import Process, Queue, Array, Lock


def consumer(queue, shared: list, lock):
    i = 0
    while True:
        res = queue.get()
        time.sleep(random.randint(1, 3))
        lock.acquire()
        print("吃了" + str(shared[i]))
        lock.release()
        i += 1
        print('\033[43m%s 吃 %s\033[0m' % (os.getpid(), res))


def producer(queue, shared: list, lock):
    for i in range(10):
        time.sleep(random.randint(1, 3))
        res = '包子%s' % i
        lock.acquire()
        print("生产了" + str(shared[i]))
        lock.release()
        queue.put(res)
        print('\033[44m%s 生产了 %s\033[0m' % (os.getpid(), res))


if __name__ == '__main__':
    q = Queue()
    l = Lock()
    arr = Array('i', [x for x in range(10)])
    print(arr)
    # 生产者们:即厨师们
    p1 = Process(target=producer, args=(q, arr, l))

    # 消费者们:即吃货们
    c1 = Process(target=consumer, args=(q, arr, l))

    # 开始
    p1.start()
    c1.start()
    print('主')
