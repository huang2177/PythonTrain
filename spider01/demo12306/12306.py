import requests

from spider01.demo12306.login_info import LoginInfo
from spider01.demo12306.order_info import OrderInfo
from spider01.demo12306.tickets_info import TicketsInfo
from spider01.demo12306.utils import get_session


def main():
    global login_helper
    # 创建session会话
    session = get_session()
    if session is None:
        session = requests.Session()

        # ========登录============
        login_helper = LoginInfo(session)
        login_helper.login()

    # ========查票============
    ticket_helper = TicketsInfo(session)
    ticket_helper.query_tickets()

    train_num = input('请输入你需要的订购的车次：')
    ticket_info = ticket_helper.get_ticket_info(train_num)

    # ========预订============
    order_helper = OrderInfo(session, ticket_info, on_login_err)
    order_helper.submit_order()


def on_login_err():
    pass
    # login_helper.login()


if __name__ == '__main__':
    main()
