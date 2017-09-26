# encoding:utf-8


import threading
import time


# def greet(index):
#     print 'hello world - %d' % index
#     time.sleep(0.5)
#
#
# def line_run():
#     for x in range(5):
#         greet(x)
#
#
# def async_run():
#     for x in range(5):
#         th = threading.Thread(target=greet, args=[x])
#         th.start()

import random


gLock = threading.Lock()
MONEY = 0


def producer():
    while True:
        global MONEY
        random_money = random.randint(10, 100)
        gLock.acquire()
        MONEY += random_money
        gLock.release()
        print '生产者%s - 生产了：%d' % (threading.current_thread, random_money)
        time.sleep(0.5)


def customer():
    while True:
        global MONEY
        random_money = random.randint(10, 100)
        if MONEY > random_money:
            print '消费者%s - 消费了：%d' % (threading.current_thread, random_money)
            gLock.acquire()
            MONEY -= random_money
            gLock.release()
        else:
            print '要消费： %d, 余额为： %d' % (random_money, MONEY)
        time.sleep(0.5)


def p_c_test():
    # 执行三个线程，作生产者
    for x in range(3):
        th = threading.Thread(target=producer)
        th.start()
    # 执行三个线程，作消费者
    for x in range(3):
        th = threading.Thread(target=customer)
        th.start()


if __name__ == "__main__":
    p_c_test()
    # async_run()



