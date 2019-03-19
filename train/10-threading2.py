# 线程（通过继承 的方式）
import threading
import time


class TestThread1(threading.Thread):
    def __init__(self, name=None):
        threading.Thread.__init__(self, name=name)

    def run(self):
        for i in range(0, 5):
            print(threading.current_thread().name, i)
            time.sleep(1)


class TestThread2(threading.Thread):
    def __init__(self, name=None):
        threading.Thread.__init__(self, name=name)

    def run(self):
        for i in range(0, 5):
            print(threading.current_thread().name, i)
            time.sleep(1)


test1 = TestThread1('TestThread1')
test2 = TestThread2('TestThread2')
test1.start()
test2.start()
