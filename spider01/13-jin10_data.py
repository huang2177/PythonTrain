# 爬取金十的数据
import time
import json
import selenium.webdriver as web

big_events_url = 'https://xnews.jin10.com/#/tag/%E5%A4%A7%E4%BA%8B%E4%BB%B6'


def get_jin10data(url):
    driver = None
    with open('out-jin10.txt', 'w') as f:
        f.write('')

    try:
        driver = web.Chrome('../chromedriver.exe')
        driver.start_client()
        driver.get(url)

        time.sleep(3)

        cards_class_name = 'news-item'
        cards = driver.find_elements_by_class_name(cards_class_name)

        for card in cards:
            c_time = card.find_element_by_class_name('news-i-other').text
            detail = card.find_element_by_tag_name('a').get_attribute('href')
            title = card.find_element_by_class_name('news-i-title').get_attribute('title')

            image_url = card.find_element_by_class_name('news-i-c') \
                            .find_element_by_tag_name('div') \
                            .get_attribute('style')[23:-3]
            if image_url:
                print(title)
                with open('out-jin10.txt', 'a', encoding='utf-8') as f:
                    data = {'title': title,
                            'detail': detail,
                            'image_url': image_url,
                            'c_time': c_time}
                    f.write(json.dumps(data) + '\n')

    finally:
        if driver is not None:
            driver.quit()


get_jin10data(big_events_url)
