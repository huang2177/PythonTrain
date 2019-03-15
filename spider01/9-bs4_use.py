# 导入
from bs4 import BeautifulSoup as BS

# 转化本地文件
soup = BS(open('in-test.html'), 'lxml')

# print(soup.img['src'])  # 只能获取第一个标签
# print(soup.div.attrs)  # 获取所有的属性
# print(soup.p.text)  # 获取内容

# print(soup.find('a', class_='contentForImage'))

# imgs = soup.find_all('img', class_=None, alt=None)
# imgs_a = soup.find_all(['img', 'a'])
# print(imgs_a)


# print(soup.select('div > img'))
print(soup.select('.imagesGif')[2]['src'])
