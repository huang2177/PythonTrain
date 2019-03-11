from urllib.request import urlopen
from datetime import date
import datetime


class Test:
    a = "world!"

    def __init__(self):
        print(self)
        print(self.__class__)

    def test(self):
        pass


if __name__ == '__main__':
    t = Test()
    t.test()

    age = int((date.today() - date(1992, 7, 7)).days / 365)
    print(age)

    # 获取昨天的日期
    print(date.today() - datetime.timedelta(1))

    # 生成日历
    import calendar

    year = int(input("请输入年份："))
    month = int(input("请输入月份："))
    print(calendar.firstweekday)
