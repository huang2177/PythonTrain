import json
import re
import time
from urllib.parse import unquote

from base.netutils import user_agent
from spider.demo12306.utils import print_response


class OrderInfo(object):
    # (secret, train_date, start_station, stop_station)
    def __init__(self, session, station_info, callback):
        self.token = ''
        self.session = session
        self.callback = callback
        self.station_info = station_info

    # 下单
    def __submit_order(self):
        # 下单之前先检查登录状态
        check_url = 'https://kyfw.12306.cn/otn/login/checkUser'
        result = self.session \
            .post(check_url, data={'_json_att': ''}, headers=user_agent) \
            .text

        flag = json.loads(result)['data']['flag']
        if not flag:
            print('登录状态异常，请重新登录！')
            # time.sleep(2)
            # self.callback()
            return

        # 下单
        submit_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'

        query_data = {
            'secretStr': unquote(self.station_info[0]['secret']),
            'train_date': self.station_info[1],
            'back_train_date': self.station_info[1],
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_to_station_name': self.station_info[3],
            'query_from_station_name': self.station_info[2],
            'undefined': ''
        }
        result = self.session.post(submit_url, data=query_data, headers=user_agent).text
        result = json.loads(result)
        print_response('提交订单', result)
        return result['status']

    def __query_contacts(self):
        # 先获取token
        html = self.__find_params()

        # 需要优化 返回的内容太多 ，此处匹配到一个就可返回
        self.token = re.findall(r"globalRepeatSubmitToken = '(.*?)'", html)[0]
        self.key_check = re.findall(r"'key_check_isChange':'(.*?)'", html)[0]
        self.left_ticket = re.findall(r"'leftTicketStr':'(.*?)'", html)[0]
        self.train_no = re.findall(r"'train_no':'(.*?)'", html)[0]
        self.from_station_code = re.findall(r"'from_station_telecode':'(.*?)'", html)[0]
        self.to_station_code = re.findall(r"'to_station_telecode':'(.*?)'", html)[0]

        if not self.token:
            return

        print_response('获取Token', self.token)
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        data = {'_json_att': '',
                'REPEAT_SUBMIT_TOKEN': self.token}
        result = self.session.post(url, data=data, headers=user_agent).text
        result = json.loads(result)
        if result['status']:
            data = result['data']['normal_passengers']
            for p in data:
                print('\n* * * * * * * * * * * * * * * * * * * * * * * ')
                print('编号 | 姓名 | 身份证 | 电话 ')
                print(f"{p['code']} | {p['passenger_name']} | {p['passenger_id_no']} | {p['mobile_no']} ")
                print('* * * * * * * * * * * * * * * * * * * * * * * \n')
            return data

    '''
    O 二等座
    M 一等座
    P 特等座
    1 硬座
    3 硬卧
    4 软卧
    '''

    # 选择座位类型
    def __select_seat_type(self):
        station = self.station_info[0]
        print('\n+ + + + + + + + + + + + + + + + + + + + + + + + +')
        print(' 车次 | 一等座(M) | 二等座(O) | 硬座(1) | 硬卧(3) ')
        print(
            f"{station['train_num']} "
            f"|  {station['seat_st']}  |  {station['seat_nd']}  |  {station['seat_yz']}  |  {station['seat_yw']}")
        print('+ + + + + + + + + + + + + + + + + + + + + + + + +  \n')

        seat_type = input('请选择座位类型（括号里面的编号）：')
        if seat_type not in ('M', 'O', '1', '3'):
            seat_type = input('输入有误！请重新选择：')

        return seat_type

    # 检查订单信息
    def __check_order_info(self, s_type, c):
        # 检查订单 1
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        passenger_str = f"{s_type},0,1," \
                        f"{c['passenger_name']},1," \
                        f"{c['passenger_id_no']}," \
                        f"{c['mobile_no']},N"
        old_passenger_str = f"{c['passenger_name']},1," \
                            f"{c['passenger_id_no']},1_"
        data = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': passenger_str,
            'oldPassengerStr': old_passenger_str,
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token,
        }
        result = self.session.post(url, data=data, headers=user_agent).text
        print_response('检查订单信息1', result)

        if json.loads(result)['status']:
            # 检查订单 2
            url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'

            train_date = self.station_info[1]
            data = {
                'train_date': 'SUn Mar 24 2019 00:00:00 GMT+0800 (中国标准时间)',
                'train_no': self.train_no,
                'statioNtraiNcode': self.station_info[0]['train_num'],
                'seaTtype': 'O',
                'froMstatioNtelecode': self.from_station_code,
                'tOstatioNtelecode': self.to_station_code,
                'lefTticket': self.left_ticket,
                'purpose_codes': '00',
                'train_location': self.station_info[0]['train_location'],
                '_json_att': '',
                'REPEAT_SUBMIT_TOKEN': self.token,
            }
            result = self.session.post(url, data=data, headers=user_agent).text
            print_response('检查订单信息2', result)

            if json.loads(result)['status']:
                # 第二个请求
                url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
                data = {
                    'passengeRtickeTstr': passenger_str,
                    'olDpassengeRstr': old_passenger_str,
                    'ranDcode': '',
                    'purpose_codes': '00',
                    'key_check_iSchange': self.key_check,
                    'lefTtickeTstr': self.left_ticket,
                    'train_location': self.station_info[0]['train_location'],
                    'choose_seats': '',
                    'seaTdetaiLtype': '000',
                    'whatSselect': '1',
                    'rooMtype': '00',
                    'dWall': 'N',
                    '_json_att': '',
                    'REPEAT_SUBMIT_TOKEN': self.token
                }
                print_response('提交订单信息', self.session.post(url, data=data, headers=user_agent).text)

    # 从页面html 有些必要参数在页面中
    def __find_params(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        html = self.session.post(url, data={'_json_att': ''}, headers=user_agent).text
        return html

    # 下单相关
    def create_order(self):
        status = self.__submit_order()
        if not status:
            print('提交订单失败，正在重新提交...')
            time.sleep(2)
            self.create_order()
            return

        contact = None
        contacts = self.__query_contacts()
        if contacts is not None:
            code = input('请输入乘客编号：')
            while True:
                for c in contacts:
                    if code == c['code']:
                        contact = c
                        break
                if contact:
                    break
                else:
                    code = input('你选择的乘客不存在，请重新输入：')

        seat_type = self.__select_seat_type()
        self.__check_order_info(seat_type, contact)
