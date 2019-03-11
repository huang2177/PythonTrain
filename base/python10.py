# 线程相关（直接实例化一个Thread）
import time
import threading


def test():
    for i in range(0, 5):
        print(threading.current_thread().name + ' test ', i)
        time.sleep(1)


test_thread = threading.Thread(target=test, name='Test')
test_thread.start()
test_thread.join()  # 会阻塞当前线程，执行完才会执行其他线程

for i in range(0, 5):
    print(threading.current_thread().name + ' main ', i)
    time.sleep(1)
