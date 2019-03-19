import requests
from base.netutils import user_agent


# 登录12306
def login():
    pass


# 检查验证码
def check():
    url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    data = {'answer': '47, 56',
            'callback': 'jQuery191012057581111562277_1553006542354',
            'rand': 'sjrand',
            'login_site': 'E',
            '_': '1553006542358'}
    r = requests.get(url, params=data, headers=user_agent)
