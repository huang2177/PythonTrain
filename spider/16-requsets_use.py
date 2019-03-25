import requests

if __name__ == '__main__':
    result = requests.get('http://www.baidu.com/')
    print(result.text)
    print(result.content)
    print(result.encoding)
    print(result.status_code)
