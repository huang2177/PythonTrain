# 线程相关（直接实例化一个Thread）
import threading
import time


def test():
    for i in range(0, 5):
        print(threading.current_thread().name + ' test ', i)
        time.sleep(1)


# daemon 意为守护线程 True：跟随主线程的生命周期
test_thread = threading.Thread(target=test, name='Test', daemon=False)
test_thread.start()
# test_thread.join()  # 会阻塞当前线程，执行完才会执行其他线程

for i in range(0, 1):
    print(threading.current_thread().name + ' main ', i)
    time.sleep(1)
