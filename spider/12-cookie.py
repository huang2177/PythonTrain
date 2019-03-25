# cookie 实际上就是服务器给浏览器的一个身份标记 类似于token

# 用来保存cookie 当请求返回cookie的时候，会自动保存，下一次访问的时候回自动带上
import http.cookiejar

import urllib.request

# 创建cookiejar对象
cj = http.cookiejar.CookieJar()

#
handler = urllib.request.HTTPCookieProcessor(cj)

opener = urllib.request.build_opener(handler)

requset = urllib.request.Request('')

opener.open(requset)
