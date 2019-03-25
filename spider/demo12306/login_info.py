import base64
import json
import time

from base.netutils import user_agent
from spider.demo12306.config import *
from spider.demo12306.utils import print_response, find_positions, save_session


# 登陆相关
class LoginInfo(object):
    def __init__(self, session):
        self.session = session
        self.data = {'callback': callback,
                     'rand': 'sjrand',
                     'login_site': 'E',
                     '_': '1553006542358'}

    # 先获取验证码
    def __get_img_code(self):
        img_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image64'
        result = self.__parse(self.session.get(img_url, params=self.data, headers=user_agent))
        print_response('验证码图片', result)

        if result['result_code'] == '0':
            print('生成验证码成功!')
        else:
            print('生成验证码失败!')
            return

        with open('code.png', 'wb') as fn:
            fn.write(base64.urlsafe_b64decode(result['image']))

    # 检查验证码
    def __check_img_code(self):
        code_str = find_positions(input('请输入验证码位置：'))
        if code_str:
            self.data.update({'answer': code_str})

            check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
            result = self.__parse(self.session.get(check_url, params=self.data, headers=user_agent))
            print_response('检查验证码', result)

            if result['result_code'] == '4':
                print('验证码检验成功！')
            else:
                print('验证码检验失败！')
        else:
            self.__check_img_code()

    # 登录12306
    def __login(self):
        location = self.data['answer'].replace(',', '%2C')
        self.data.update({
            'username': user,
            'password': pwd,
            'appid': 'otn',
            'answer': location
        })
        login_url = 'https://kyfw.12306.cn/passport/web/login'
        result = self.__parse(self.session.post(login_url, data=self.data, headers=user_agent))
        print_response('登录', result)

        if result['result_code'] == 0:
            print('登录成功！')
            return self.__check_login_status()
        else:
            print('登录失败，请重新登录！')
            time.sleep(2)
            self.__get_img_code()
            self.__check_img_code()
            self.__login()
            return False

    # 登录成功后还要调用几个接口
    # 去检查是否真的登陆成功，否则后续下单失败
    def __check_login_status(self):
        # ========检验1=========
        url = 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        self.session.post(url, headers=user_agent)

        # ========检验2=========
        url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        self.session.post(url, headers=user_agent)

        # ========检验3=========
        data = {'appid': 'otn'}
        url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        result = json.loads(self.session.post(url, data=data, headers=user_agent).text)
        print_response('检验3', result)

        if result['result_code'] != 0:
            return
        tk = result['newapptk']

        # ========检验4=========
        data = {'tk': tk}
        url = 'https://kyfw.12306.cn/otn/uamauthclient'
        result = json.loads(self.session.post(url, data=data, headers=user_agent).text)
        print_response('检验4', result)

        if result['result_code'] != 0:
            self.login()
            return

        save_session(self.session)
        print('登录检验成功，欢迎您，', result['username'])
        print('\n=============================================')

    def __parse(self, result):
        return json.loads(result.text[len(callback) + 5:-2])

    # ==================登录相关====================
    def login(self):
        self.__get_img_code()
        self.__check_img_code()
        self.__login()
