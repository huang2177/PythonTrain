# 通过正则的方式匹配到图片 然后下载

import re
import os
import urllib.request

url = 'https://www.qiushibaike.com/pic/page/3/?s=5174318'


def handle_request():
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    }
    return urllib.request.Request(url, headers=headers)


# <div class="thumb">
# <a href="/article/121603055" target="_blank">
# <img src="//pic.qiushibaike.com/system/pictures/12160/121603055/medium/6UIHOZX767BTIGAG.jpg" alt="为什么他们如此优秀">
# </a>
# </div>


def create_folder():
    if not os.path.exists('images'):
        os.mkdir('images')
    return 'images'


def download(content):
    path = create_folder()

    pattern = re.compile(r'<div class="content-text">.*?<img src="(.*?)">.*?</div>', re.S)
    lt = pattern.findall(content)

    for src in lt:
        if not ' ' in src:
            src = "https:" + src
            print(src)
            file_name = src.split('/')[-1] + '.jpg'
            file_path = path + '/' + file_name
            urllib.request.urlretrieve(src, file_path)


def get_html():
    response = urllib.request.urlopen(handle_request())
    return response.read().decode()


download(get_html())
