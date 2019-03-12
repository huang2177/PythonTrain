# https://sou.zhaopin.com/?p=2&jl=%E4%B8%8A%E6%B5%B7&sf=15001&st=25000&kw=Python&kt=3

import urllib.parse
import urllib.request
from bs4 import BeautifulSoup as BS


class ZhiLianSpider(object):
    url = 'https://sou.zhaopin.com/?'

    def __init__(self, jl, kw):
        self.jl = jl
        self.kw = kw

    def handle_request(self, page):
        data = {
            'jl': self.jl,
            'kw': self.kw,
            'p': page,
            'sf': 15001,
            'st': 25000,
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'urlfrom2=121113803; adfbid2=0; sts_deviceid=1690e9421014b1-06e608213d64ee-3a3a5c0e-2073600-1690e9421021; urlfrom=121113803; adfbid=0; ZP_OLD_FLAG=false; dywec=95841923; __utmc=269921210; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1550727783,1552370868; sts_sg=1; sts_chnlsid=121113803; zp_src_url=https%3A%2F%2Fsp0.baidu.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc.php%3Ft%3D06KL00c00fZmx9C0E3w90KqiAsjmHcIT00000rXdj-C00000V2I6e6.THLyktAJdIjA80K85yF9pywdpAqVuNqsusK15yfdPjwBnW-Bnj0sP19WPvc0IHdawjfLfH9jP17afHujPDczwbwan1DvPWPaf1cYPHPKn6K95gTqFhdWpyfqn1D4PHczPjb3PiusThqbpyfqnHm0uHdCIZwsT1CEQLILIz4lpA7ETA-8QhPEUHq1pyfqnHcknHD1rj01FMNYUNq1ULNzmvRqmh7GuZNsmLKlFMNYUNqVuywGIyYqmLKY0APzm1Y1njcsP6%26tpl%3Dtpl_11535_18778_14772%26l%3D1510913511%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E5%252587%252586%2525E5%2525A4%2525B4%2525E9%252583%2525A8-%2525E6%2525A0%252587%2525E9%2525A2%252598-%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E3%252580%252590%2525E6%252599%2525BA%2525E8%252581%252594%2525E6%25258B%25259B%2525E8%252581%252598%2525E3%252580%252591%2525E5%2525AE%252598%2525E6%252596%2525B9%2525E7%2525BD%252591%2525E7%2525AB%252599%252520%2525E2%252580%252593%252520%2525E5%2525A5%2525BD%2525E5%2525B7%2525A5%2525E4%2525BD%25259C%2525EF%2525BC%25258C%2525E4%2525B8%25258A%2525E6%252599%2525BA%2525E8%252581%252594%2525E6%25258B%25259B%2525E8%252581%252598%2525EF%2525BC%252581%2526xp%253Did(%252522m3195224985_canvas%252522)%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D228%26wd%3D%25E6%2599%25BA%25E8%2581%2594%25E6%258B%259B%25E8%2581%2598%26issp%3D1%26f%3D8%26ie%3Dutf-8%26rqlang%3Dcn%26tn%3Dbaiduhome_pg%26inputT%3D2796; _jzqa=1.4578407057055315500.1550727783.1550727783.1552370868.2; _jzqc=1; _jzqy=1.1550727783.1552370868.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; _jzqckmp=1; firstchannelurl=https%3A//passport.zhaopin.com/login; lastchannelurl=https%3A//ts.zhaopin.com/jump/index_new.html%3Futm_source%3Dbaidupcpz%26utm_medium%3Dcpt%26utm_provider%3Dpartner%26sid%3D121113803%26site%3Dnull; JsNewlogin=2003854121; JSloginnamecookie=15378412400%40163%2Ecom; JSShowname=%E9%BB%84%E5%8F%8C; at=05ebde09beee4719bb62ba4a0c0c0013; Token=05ebde09beee4719bb62ba4a0c0c0013; rt=1f80cc6839ad4c81b69dabff3bfb3dfe; JSpUserInfo=386b2e6956714165597002694c6d5e6a586b4277526f43355275216b2469567146655a700669426d536a5d6b4077576f443559755d6b2a695a7141655c701b69166d046a046b4a77306f3e355475a9f5a63a5071326522700869446d5e6a5a6b46775d6f443558755f6b5e695b7147652f700469436d586a476b12770a6f1d3552753e6b3e695671466554707469216d566a5b6b5c77576f50355875596b506953714c652e707969486d5a6a526b2477246f4d352375206b5c695c714e655a700469466d5c6a5a6b47775e6f25353d75506b5b695071246526700869456d506a9; uiioit=2264202c55795c690e374279516b4264552c5b795d690b374e792a6b3364592c587951695; jobRiskWarning=true; LastCity=%E4%B8%8A%E6%B5%B7; LastCity%5Fid=538; acw_tc=2760820915523709273776685e29aab4cfbb30d63edd64d449d96dc98d6a9c; sts_sid=16970a2c58682-025a11b4f4e1e1-2d604637-304500-16970a2c5871ca; dywea=95841923.1272849551550307300.1550727783.1552370868.1552373223.3; dywez=95841923.1552373223.3.3.dywecsr=sou.zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/; __utma=269921210.2021336562.1550727783.1552370868.1552373223.3; __utmz=269921210.1552373223.3.3.utmcsr=sou.zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/; loginreleased=1; dyweb=95841923.3.10.1552373223; __utmt=1; __utmb=269921210.3.10.1552373223; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22667951373%22%2C%22%24device_id%22%3A%221690e942044b8-0c8662f0dc8e4c-3a3a5c0e-2073600-1690e9420453b3%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidupcpz%22%2C%22%24latest_utm_medium%22%3A%22cpt%22%7D%2C%22first_id%22%3A%221690e942044b8-0c8662f0dc8e4c-3a3a5c0e-2073600-1690e9420453b3%22%7D; ZL_REPORT_GLOBAL={%22sou%22:{%22actionid%22:%22d4d61d48-5c36-4466-a0a6-86e5f9e62bad-sou%22%2C%22funczone%22:%22smart_matching%22}%2C%22//jobs%22:{%22actionid%22:%22816e23f8-fe01-41cd-ba23-01cfe4b2cd01-jobs%22%2C%22funczone%22:%22dtl_best_for_you%22}}; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1552374525; sts_evtseq=12',
            'DNT': '1',
            'Host': 'sou.zhaopin.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        self.url += urllib.parse.urlencode(data)
        print(self.url)
        req = urllib.request.Request(self.url, headers=headers)
        return urllib.request.urlopen(req).read().decode()

    def parse_content(self, html):
        jobs = []
        soup = BS(open('zhilian.html', 'r', encoding='utf-8'), 'lxml')
        content = soup.find('div', id='listContent')
        cards = content.select('.contentpile__content__wrapper__item ')
        for card in cards:
            job_name = card.find('div', class_='contentpile__content__wrapper__item__info__box__jobname')
            saray = card.find('p', class_='contentpile__content__wrapper__item__info__box__job__saray')
            demand = card.find('li', class_='contentpile__content__wrapper__item__info__box__job__demand__item')

            with open('python_jobs.txt', 'a', encoding='utf-8') as f:
                f.write(job_name.text.strip().replace("\n", "")
                        + ' : ' + saray.text.strip().replace("\n", "")
                        + ':' + demand.text.strip().replace("\n", "") + '\n')

    def run(self):
        data = []
        for i in range(1, 2):
            html = self.handle_request(i)
            self.parse_content(html)


if __name__ == '__main__':
    zhiLian = ZhiLianSpider('上海', 'Python')
    zhiLian.parse_content('')
