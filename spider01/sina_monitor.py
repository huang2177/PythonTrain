# 实时监测某条微博的数据
import time
import selenium.webdriver as wd

url = 'https://weibo.com/2081681517/HiXo0vTJC?ref=feedsdk&type=comment#_rnd1551541284632'


def start_chrome():
    driver = wd.Chrome(executable_path='D:/PythonProject/chromedriver.exe')
    driver.start_client()
    return driver


def access_web():
    driver.get(url)


def find_info():
    # css_selector
    sel = 'span > span > span > em:nth-child(2)'
    elem = driver.find_elements_by_css_selector(sel)
    return [int(el.text) for el in elem[1:]]


while True:
    driver = start_chrome()
    access_web()
    time.sleep(5)  # wait loading (会去验证是否是游客之类的)
    info = find_info()
    print(info)
    time.sleep(60)
