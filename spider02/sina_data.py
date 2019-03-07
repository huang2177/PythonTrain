# 获取微博某大V某一时间段的微博数据

import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def start_chrome():
    driver = webdriver.Chrome(executable_path='D:/PythonProject/chromedriver.exe')
    driver.start_client()
    return driver


def input_data(s_time, e_time):
    return f'https://weibo.com/qinlan?is_ori=1&key_word=&start_time={s_time}&end_time={e_time}&is_search=1&is_searchadv=1#_0'


def scroll_down():
    html_page = driver.find_element_by_tag_name('html')
    for i in range(10):
        html_page.send_keys(Keys.END)
        time.sleep(0.6)


def find_card_info():
    info_list = []
    card_sel = 'div.WB_feed_detail.clearfix'
    cards = driver.find_elements_by_css_selector(card_sel)
    while not cards:
        cards = driver.find_elements_by_css_selector(card_sel)
        time.sleep(2)
        print('请求失败！')

    for card in cards:
        time_sel = 'div.WB_from.S_txt2'
        link_sel = 'div.WB_from.S_txt2 > a:nth-child(1)'
        content_sel = 'div.WB_detail > div.WB_text.W_f14'

        time1 = card.find_element_by_css_selector(time_sel)
        link = card.find_element_by_css_selector(link_sel)
        content = card.find_element_by_css_selector(content_sel)

        info_list.append([content.text, time1.text, link.get_attribute('href')])
    return info_list


def save(info_lsit, name):
    full_path = f'D:{name}.csv'
    if os.path.exists(full_path):
        with open(full_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerows(info_lsit)
    else:
        with open(full_path, 'w+') as f:
            writer = csv.writer(f)
            writer.writerows(info_lsit)


def find_next():
    next_sel = 'div:nth-child(54) > div > a'
    next_page = driver.find_elements_by_css_selector(next_sel)

    if next_page:
        return next_page[0].get_attribute('href')


def run_crawler():
    input()
    driver.get(input_data('2019-01-01', '2019-03-03'))
    time.sleep(3)
    scroll_down()
    time.sleep(3)
    info_list = find_card_info()
    save(info_list, '2019')
    if find_next():
        run_crawler()


driver = start_chrome()
run_crawler()
