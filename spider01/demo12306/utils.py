# -*- coding: utf-8 -*-
import pickle

from spider01.demo12306.config import enable_print, code_positions
from spider01.demo12306.config import station_str, session_file


# 将session保存起来
def save_session(session):
    with open(session_file, 'wb') as fn:
        pickle.dump(session, fn)


# 从文件获取session
def get_session():
    try:
        with open(session_file, 'rb') as fn:
            return pickle.load(fn)
    except:
        return None


# 打印返回结果
def print_response(type_str, response):
    if enable_print:
        print('\n=============================================')
        print(type_str, response)


# 根据顺序获取验证码位置信息（x，y）
def find_positions(position):
    code_str = ''
    for p in position.split(','):
        p = int(p)
        if p <= 0 or p > 8:
            print('输入位置错误！')
            return None

        code_str += code_positions[p - 1][0] + ',' + code_positions[p - 1][1] + ','
    return code_str[:-1]


# 找到对应的车站代号
def find_station_tag(station_name):
    stations_dict = {}
    stations = station_str.split('@')[1:]

    for s in stations:
        s_list = s.split('|')
        stations_dict[s_list[0]] = s_list[2]
        stations_dict[s_list[1]] = s_list[2]
        stations_dict[s_list[3]] = s_list[2]
        stations_dict[s_list[4]] = s_list[2]

        if station_name in stations_dict.keys():
            return stations_dict[station_name]
