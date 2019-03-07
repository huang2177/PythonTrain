import urllib.request as r
import urllib.parse as p


# 利用urlopen/request下载一张图片
def download_cat():
    # urlopen的第二个参数 不传则表示get请求 有值则表示post
    response = r.urlopen('http://placekitten.com/g/200/300')
    img = response.read()
    with open('D:/cat_200.jpg', 'wb') as f:
        f.write(img)

    print(response.info())
    print(response.geturl())
    print(response.getcode())


def translate():
    query = input('请输入需要翻译的内容（按q!退出！）：')

    _to = 'zh' if (isinstance(query, str)) else 'en'
    _from = 'en' if (isinstance(query, str)) else 'zh'

    data = {'from': 'AUTO',
            'to': 'AUTO',
            'i': query,
            'keyfrom': 'fanyi.web',
            'doctype': 'json',
            'xmlVersion': '1.6',
            'client': 'fanyideskweb',
            'salt': '15514344202583',
            'sign': '1e5324751332059ae2d2150643536f57',
            'ts': '1551434420258',
            'bv': '4d481d4d8377a582edf0317af9acd826',
            'version': '2.1',
            'action': 'FY_BY_REALTIME',
            'typoResult': 'false'}

    data = p.urlencode(data).encode('utf-8')
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    head = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
                      'Version/11.0 Mobile/15A372 Safari/604.1'}
    req = r.Request(url, data, head)
    response = r.urlopen(req)
    html = response.read().decode('utf-8')
    print(html)


if __name__ == '__main__':
    # download_cat()
    translate()
