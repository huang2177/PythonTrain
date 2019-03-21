import re
import json
import time

from urllib.parse import unquote

from base.netutils import user_agent
from spider01.demo12306.utils import print_response


class OrderInfo(object):
    # (secret, train_date, start_station, stop_station)
    def __init__(self, session, ticket_info, callback):
        self.session = session
        self.secret = ticket_info[0]
        self.train_date = ticket_info[1]
        self.start_station = ticket_info[2]
        self.stop_station = ticket_info[3]
        self.callback = callback

    # 下单
    def submit_order(self):
        # 下单之前先检查登录状态
        check_url = 'https://kyfw.12306.cn/otn/login/checkUser'
        result = self.session \
            .post(check_url, data={'_json_att': ''}, headers=user_agent) \
            .text

        flag = json.loads(result)['data']['flag']
        if not flag:
            print('登录状态异常，请重新登录！')
            time.sleep(2)
            self.callback()
            return

        # 下单
        submit_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'

        query_data = {
            'secretStr': unquote(self.secret),
            'train_date': self.train_date,
            'back_train_date': self.train_date,
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_to_station_name': self.stop_station,
            'query_from_station_name': self.start_station,
            'undefined': ''
        }
        result = self.session.post(submit_url, data=query_data, headers=user_agent).text
        result = json.loads(result)
        print_response('提交订单', result)
        if result['status']:
            self.query_contacts()

    def query_contacts(self):
        # 先获取token
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        html = self.session.post(url, headers=user_agent).text

        # 需要优化 返回的内容太多 ，此处匹配到一个就可返回
        token = re.findall(r"globalRepeatSubmitToken = '(.*?)'", html)[0]

        if not token:
            return

        print_response('获取Token', token)
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        data = {'_json_att': '',
                'REPEAT_SUBMIT_TOKEN': token}
        result = self.session.post(url, data=data, headers=user_agent).text
        print_response('获取联系人', result)
        result = json.loads(result)
        if result['status']:
            print('获取联系人成功！')
            data = result['data']['normal_passengers']
            for (p, i) in data:
                print('\n- - - - - - - - - - - - - - - - - - - - - - - ')
                print('编号 | 姓名 | 身份证 | 电话 ')
                print(f"{i} | p{['passenger_name']} | {p['passenger_id_no']} | {p['mobile_no']} ")
                print('- - - - - - - - - - - - - - - - - - - - - - - \n')
