import requests

from spider.demo12306.login_info import LoginInfo
from spider.demo12306.order_info import OrderInfo
from spider.demo12306.tickets_info import TicketsInfo
from spider.demo12306.utils import get_session, save_session


class T12306(object):
    def __init__(self):
        self.login_helper = None

    def main(self):
        # 创建session会话
        session = get_session()
        if session is None:
            session = requests.Session()

            # ========登录============
            self.login_helper = LoginInfo(session)
            self.login_helper.login()

        # ========查票============
        ticket_helper = TicketsInfo(session)
        ticket_helper.query_tickets()

        train_num = input('请输入你需要的订购的车次：')
        ticket_info = ticket_helper.get_ticket_info(train_num)

        # ========预订============
        order_helper = OrderInfo(session, ticket_info, self.on_login_err)
        order_helper.create_order()

    def on_login_err(self):
        save_session(None)
        self.main()


if __name__ == '__main__':
    T12306().main()
