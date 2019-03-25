import os
import time
import selenium.webdriver as web

url = 'https://www.xicidaili.com/nn/'


def start_chrome():
    _driver = web.Chrome('D:/pythonprojects/PythonTrain01/chromedriver.exe')
    _driver.start_client()
    return _driver


def get_ip():
    ips = []
    td_sel = '#ip_list > tbody > tr'
    tds = driver.find_elements_by_css_selector(td_sel)

    for td in tds[1:]:
        ip_sel = 'td:nth-child(2)'
        port_sel = 'td:nth-child(3)'

        ip = td.find_element_by_css_selector(ip_sel).text
        port = td.find_element_by_css_selector(port_sel).text
        ips.append(f'{ip}:{port}')

    return ips


def save(ips):
    ips = '\n'.join(ips) + '\n'
    if os.path.exists('proxy.txt'):
        with open('proxy.txt', 'a') as f:
            f.write(ips)
    else:
        with open('proxy.txt', 'w+') as f:
            f.write(ips)


def find_next():
    for i in range(1, 4):
        driver.get(url + str(i))
        time.sleep(3)
        save(get_ip())
        print(f'获取第{i}页数据')


driver = start_chrome()
find_next()
