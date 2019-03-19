from queue import Queue

# 长度可选
queue = Queue(5)

queue.put(1)
queue.put(2)
queue.put(3)
queue.put(4)
queue.put(5)
# queue.put(6)  # 如果queue已经满了，则会卡在着了，直到queue有取出；
# queue.put(6, False)  # 如果queue已经满了，则会直接报错；
# queue.put(6, True, 3)  # 如果queue已经满了，会等待3秒，若还是没有空位置，则报错；

print(queue.get())

print(queue)
