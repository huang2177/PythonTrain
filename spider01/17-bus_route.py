import requests
from base.netutils import *
from bs4 import BeautifulSoup as bs4

url = 'https://shanghai.8684.cn'


# 获取第一页导航的链接
def parse_nav(in_str):
    if in_str.isdigit():
        nav_sel = '.bus_kt_r1'
    elif in_str.isalpha():
        in_str = in_str.upper()
        nav_sel = '.bus_kt_r2'
        return
    else:
        print('暂支持输入数字！！')
        return

    r = requests.get(url, headers=user_agent)
    soup = bs4(r.text, 'lxml')
    navs = soup.select(nav_sel)[0].find_all('a')
    for a in navs:
        if a.text == in_str[0]:
            return {a.text: a['href']}


# 根据第一步得到导航找到相关的公交线路
def parse_more_bus(in_str, nav):
    method = nav[in_str[0]]
    r = requests.get(url + method, headers=user_agent)
    soup = bs4(r.text, 'lxml')
    routes = soup.select('#con_site_1')[0].find_all('a')
    for a in routes:
        if in_str == a.text:
            return {a.text: a['href']}


# 获取具体的公交路线信息
def detail_info(bus):
    method = list(bus.values())[0]
    r = requests.get(url + method, headers=user_agent)
    soup = bs4(r.text, 'lxml')
    route_name = soup.find('div', class_='bus_line_txt').find('strong').text
    layers = soup.select('.bus_site_layer')[0].find_all('div')

    # with open('bus_route.txt', 'w+', encoding='utf-8')as f:
    #     f.write(route_name + '\n')

    print(route_name + '\n')

    for layer in layers:
        num = layer.find('i').text
        station_name = layer.find('a').text

        # with open('bus_route.txt', 'a', encoding='utf-8')as f:
        #     f.write(num + ' : ' + station_name + '\n')
        print(num + ' : ' + station_name)


def main():
    try:
        in_str = input('请输入要查询的公交：')
        nav = parse_nav(in_str)
        bus = parse_more_bus(in_str, nav)
        detail_info(bus)
    except Exception as e:
        print(e)
        print('查询失败或无次公交车')


if __name__ == '__main__':
    main()
