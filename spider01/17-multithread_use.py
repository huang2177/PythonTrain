# 多线程爬取
import json
import threading
import time
from queue import Queue
from threading import Thread

import requests
from bs4 import BeautifulSoup as bs

# 用来存储数据
result = []

# 需要爬取的总页码
page_count = 11

# 用来存放采集、解析线程
g_crawl_list = []
g_parse_list = []


# 采集线程
class CrawlThread(Thread):
    def __init__(self, name, page_queue, data_queue):
        Thread.__init__(self)
        self.name = name
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.url = 'http://www.fanjian.net/jiantu-{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }

    def run(self):
        print(f'{self.name}启动！！！')
        while True:
            # 当所有页码都爬取了，就退出循环
            if self.page_queue.empty():
                break

            # 拼接url
            page = self.page_queue.get()
            url = self.url.format(page)
            # 发送请求
            r = requests.get(url, headers=self.headers)
            # # 将响应放到data_queue
            data = (page, r.text)
            self.data_queue.put(data)

        print(f'{self.name}结束！！！')


# 解析线程
class ParseThread(Thread):
    def __init__(self, name, data_queue, fb, lock):
        Thread.__init__(self)
        self.name = name
        self.fb = fb
        self.lock = lock
        self.data_queue = data_queue
        self.ending = False

    def run(self):
        print(f'{self.name}启动！！！')
        while not self.ending:
            data = self.data_queue.get()

            # 解析内容
            self.parse_content(data)

            # if data[0] == page_count - 1:
            #     for tparse in g_parse_list:
            #         tparse.ending = True

        print(f'{self.name}结束！！！')

    def parse_content(self, data):
        items = []
        global img_url, title
        soup = bs(data[1], 'lxml')

        title_divs = soup.find_all('div', class_='cont-list-tc')
        for div in title_divs:
            title = div.text

        img_divs = soup.find_all('div', class_='cont-list-main')
        for div in img_divs:
            img_attrs = dict(div.find('img').attrs)
            if 'src' in img_attrs.keys():
                img_url = img_attrs['src']
            elif 'data-src' in img_attrs.keys():
                img_url = img_attrs['data-src']
            else:
                img_url = ''

            items.append({
                'page': data[0],
                'title': title,
                'image_url': img_url + '\n'
            })

        self.lock.acquire()
        result.append(items)
        self.lock.release()


def create_queue():
    # 创建页码队列
    page_queue = Queue()
    for i in range(1, page_count):
        page_queue.put(i)

        # 创建内容队列
    data_queue = Queue()
    return page_queue, data_queue


def create_crawl_thread(page_queue, data_queue):
    crawl_name = ['采集线程1', '采集线程2', '采集线程3']
    for name in crawl_name:
        tcrawl = CrawlThread(name, page_queue, data_queue)
        g_crawl_list.append(tcrawl)
        tcrawl.start()


def create_parse_thread(data_queue, fb, lock):
    parse_name = ['解析线程1', '解析线程2', '解析线程3']
    for name in parse_name:
        tparse = ParseThread(name, data_queue, fb, lock)
        g_parse_list.append(tparse)
        tparse.start()


def main():
    page_queue, data_queue = create_queue()

    time.sleep(2)

    create_crawl_thread(page_queue, data_queue)

    time.sleep(2)
    lock = threading.Lock()
    fb = open('out-jiantu.txt', 'a')
    create_parse_thread(data_queue, fb, lock)

    for tcrawl in g_crawl_list:
        tcrawl.join()

    for tparse in g_parse_list:
        tparse.join()

    print('主线程执行')


if __name__ == '__main__':
    main()
