import base64
import json
import ssl
import time

import requests

from base.netutils import user_agent
from spider01.demo12306.config import *

# 创建session会话
req = requests.Session()

data = {'callback': callback,
        'rand': 'sjrand',
        'login_site': 'E',
        '_': '1553006542358'}

ssl._create_default_https_context = ssl._create_unverified_context


# 先获取验证码
def get_img_code():
    img_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image64'
    result = parse(req.get(img_url, params=data, headers=user_agent))

    if result['result_code']:
        print('生成验证码成功!')
    else:
        print('生成验证码失败!')
        return

    with open('code.png', 'wb') as fn:
        fn.write(base64.urlsafe_b64decode(result['image']))


# 检查验证码
def check_img_code():
    data.update({'answer': input('请输入验证码位置：')})
    check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    result = parse(req.get(check_url, params=data, headers=user_agent))

    if result['result_code']:
        print('验证码检验成功！')
    else:
        print('验证码检验失败！')


# 登录12306
def login():
    location = data['answer'].replace(',', '%2C')
    data.update({
        'username': user,
        'password': pwd,
        'appid': 'otn',
        'answer': location
    })
    login_url = 'https://kyfw.12306.cn/passport/web/login'
    login_info = parse(req.post(login_url, data=data, headers=user_agent))

    if login_info['result_code']:
        print('登录成功！')
    else:
        print('登录失败！')


def parse(result):
    return json.loads(result.text[len(callback) + 5:-2])


# [3] 车次
# [8] 出发时间
# [9] 达到时间
# [10] 历时
# [23] 软卧一等卧
# [23] 软卧一等卧
# [26] 无座
# [28] 硬卧二等卧
# [29] 硬座
# [30] 二等座
# [31] 一等座

train_date = '2019-03-21'
start_station_name = '重庆'
stop_station_name = '成都'


# 查询余票
def query_tickets():
    url = 'https://kyfw.12306.cn/otn/leftTicket/query'
    start_station_name = find_station_tag(input('请输入起始站：'))
    stop_station_name = find_station_tag(input('请输入终点站：'))
    if start_station_name is None:
        start_station_name = find_station_tag(input('没有该车站，请重新输入：'))

    if start_station_name is None:
        stop_station_name = find_station_tag(input('没有该车站，请重新输入：'))

    train_date = time.strftime("%Y-%m-%d", time.localtime())

    params = {
        'leftTicketDTO.train_date': train_date,
        'leftTicketDTO.from_station': start_station_name,
        'leftTicketDTO.to_station': stop_station_name,
        'purpose_codes': 'ADULT'
    }

    result = req.get(url, params=params, headers=user_agent).text
    result = (json.loads(result))['data']['result']
    if not len(result):
        print('暂未查询到该路线的列车！')
        return

    for item in result:
        ticket = item.split('|')
        if (ticket[29] == '无' or ticket[29] == '--') \
                and (ticket[30] == '无' or ticket[30] == '--') \
                and (ticket[31] == '无' or ticket[31] == '--'):
            print('该路线的列车暂无余票！')
            return

        print('车次 | 出发时间 | 历时 | 一等座 | 二等座 | 硬座 ')
        print(f'{ticket[3]} | {ticket[8]} | {ticket[10]} | {ticket[31]} | {ticket[30]} | {ticket[29]} ')
        print('\n----------------------------------------------\n')


# 下单
def create_order():
    # 下单之前先检查登录状态
    check_url = 'https://kyfw.12306.cn/otn/login/checkUser'
    result = req.post(check_url, data={'_json_att': ''}, headers=user_agent).text
    status = json.loads(result)['status']
    if not status:
        print('登录状态异常，请重新登录！')
        return

    # 下单
    submit_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
    data = {
        'secretStr': '1JzyeW4Qz1gsAmZWa6aGUHRXklriCLMNxvfECOjTJk4PTkN639A1T7JbGYTA6FpsMj3oX0Iec01GmFsR'
                     '/g2NT3+QEKfPx6NXsb3qT8o4OhRb1kVUmp2nejAjuvQ3X9lalxv1GVhCkFFUe3M8OXFuTGEqyCjrz3Ei'
                     '9WrOta9IAl0adNKQSzT+T8/Pj5Oy5RonIJ4eVP+zU1fXF/1y+m/SV3OY1XXOJeG9abJ3/kW9Ok6t5qkj'
                     'wXjirOcLAGpbO+prZTv1fUsunFRYU2SWxt3JmRcbHX9Hcvl/PRFIVy6++20kOS57',
        'train_date': train_date,
        'back_train_date': train_date,
        'tour_flag': 'dc',
        'purpose_codes': 'ADULT',
        'query_from_station_name': start_station_name,
        'query_to_station_name': stop_station_name,
        'undefined': ''
    }

    print(req.post(submit_url, data=data, headers=user_agent).text)


if __name__ == '__main__':
    # get_img_code()
    # check_img_code()
    # login()
    # input('')
    # query_tickets()
    create_order()
