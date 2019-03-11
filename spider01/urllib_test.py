import urllib.request as request
import urllib.parse as parse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# response = request.urlopen('https://www.baidu.com/')
# with open('./baidu.html', 'wb') as file:
#     file.write(response.read())

# headers = {'user-agent': 'Huang'}
# req = request.Request('http://www.baidu.com/', None, headers)
# response = request.urlopen(req)
# with open('./baidu1.html', 'wb') as file:
#     file.write(response.read())


headers = {'user-agent': 'Huang'}
data = {'name': 'Huang', 'age': '26'}
# 队请求的参数进行编码
query = parse.urlencode(data)

req = request.Request('http://www.baidu.com/', query, headers)
response = request.urlopen(req)
