import urllib.request as r

import urllib.parse as  p

headers = {}
url = 'http://www.baidu.com/'

handler = r.HTTPHandler()

opener = r.build_opener(handler)

request = r.Request(url, headers=headers)

response = opener.open(request)

print(response.read().decode())
