# 爬取知乎神回复

import urllib.parse as parse
import urllib.request as request

topic_id = '19550517'
url = f'https://www.zhihu.com/topic/{topic_id}/top-answers'

response = request.urlopen(url)
print(response.read())
