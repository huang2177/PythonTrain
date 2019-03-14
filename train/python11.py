# 线程（通过继承 的方式）
import time
import threading


class TestThread(threading.Thread):
    def __init__(self, name=None):
        threading.Thread.__init__(self, name=name)

    def run(self):
        for i in range(0, 5):
            print(threading.current_thread().name + ' Test', i)
            time.sleep(1)


test = TestThread('TestThread')
test.start()
