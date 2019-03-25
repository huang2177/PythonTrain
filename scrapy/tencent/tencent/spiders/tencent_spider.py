# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs


class TencentSpiderSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        soup = bs(response.text, 'lxml')
        tr_list = soup.find('table', class_='tablelist').find_all('tr')[1:-1]
        item = {}
        for tr in tr_list:
            td_list = tr.find_all('td')
            item['job_name'] = td_list[0].text
            item['job_type'] = td_list[1].text
            item['job_location'] = td_list[3].text
            yield item

        next_url = soup.find('a', id='next')['href']
        if next_url != 'javascript:;':
            next_url = 'https://hr.tencent.com/' + next_url
            yield scrapy.Request(next_url, self.parse)
