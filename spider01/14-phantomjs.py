import time
import selenium.webdriver as web
from selenium.webdriver.chrome.options import Options


def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = web.PhantomJS(executable_path='../phantomjs.exe')
    # driver = web.Chrome(executable_path='../chromedriver.exe')

    driver.get('https://weibo.com/')
    time.sleep(8)
    driver.save_screenshot('images/weibo1.png')

    # 执行代码 页面滚动到底部
    js = 'document.body.scrollTop=10000'
    driver.execute_script(js)
    time.sleep(5)
    driver.save_screenshot('images/weibo2.png')
    html = driver.page_source  # 网页代码 (html)

    driver.close()


if __name__ == '__main__':
    main()
