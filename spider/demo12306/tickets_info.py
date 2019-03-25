import json
import ssl
import time

from base.netutils import user_agent
from spider.demo12306.utils import find_station_tag

'''
[3] 车次
[8] 出发时间
[9] 达到时间
[10] 历时
[15] train_location
[23] 软卧一等卧
[26] 无座
[28] 硬卧二等卧
[29] 硬座
[30] 二等座
[31] 一等座
'''


class TicketsInfo(object):

    def __init__(self, session):
        self.station_info = []
        self.session = session

        self.train_date = ''
        self.stop_station = ''
        self.start_station = ''
        ssl._create_default_https_context = ssl._create_unverified_context

    # 查询余票
    def query_tickets(self):
        url = 'https://kyfw.12306.cn/otn/leftTicket/query'

        self.start_station = find_station_tag(input('请输入起始站：'))
        if self.start_station is None:
            self.start_station = find_station_tag(input('没有该车站，请重新输入起始站：'))

        self.stop_station = find_station_tag(input('请输入终点站：'))
        if self.start_station is None:
            self.stop_station = find_station_tag(input('没有该车站，请重新输入终点站：'))

        self.train_date = '2019-03-24'

        params = {
            'leftTicketDTO.train_date': self.train_date,
            'leftTicketDTO.from_station': self.start_station,
            'leftTicketDTO.to_station': self.stop_station,
            'purpose_codes': 'ADULT'
        }

        result = self.session.get(url, params=params, headers=user_agent).text
        result = (json.loads(result))['data']['result']
        if not len(result):
            print('暂未查询到该路线的列车！')
            return

        for item in result:
            ticket = item.split('|')
            seat_st = self.show(ticket, 31)
            seat_nd = self.show(ticket, 30)
            seat_yz = self.show(ticket, 29)
            seat_yw = self.show(ticket, 28)
            if seat_st == '--' and seat_nd == '--' and seat_yz == '--' and seat_yw == '--':
                return

            print('\n+ + + + + + + + + + + + + + + + + + + + + + + + + + + ')
            print(' 车次 | 出发时间 | 历时 | 一等座 | 二等座 | 硬座 | 硬卧  ')
            print(f' {ticket[3]} | {ticket[8]} | {ticket[10]} |  {seat_st}  |   {seat_nd}  |  {seat_yz}  |  {seat_yw} ')
            print('+ + + + + + + + + + + + + + + + + + + + + + + + + + + \n')

            self.station_info.append({'secret': ticket[0],
                                      'train_num': ticket[3],
                                      'train_location': ticket[15],
                                      'seat_st': self.show(ticket, 31),
                                      'seat_nd': self.show(ticket, 30),
                                      'seat_yz': self.show(ticket, 29),
                                      'seat_yw': self.show(ticket, 28), })

    def show(self, ticket, index):
        if 0 <= index < len(ticket):
            result = ticket[index]
            if result == '' or result == '无':
                result = '--'
            return result

    # 获取预订车票的相关信息
    # (secret, train_date, start_station_name, stop_station_name)
    def get_ticket_info(self, train_num):
        for station in self.station_info:
            if train_num == station['train_num']:
                return station, self.train_date, self.start_station, self.stop_station
        else:
            return self.get_ticket_info(input('你输入的车次有误！请重新输入：'))
