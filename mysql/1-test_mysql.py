from mysql import connector


def connect():
    conn = connector.connect(user='root', password='root', database='huang', use_unicode=True)
    # 运行查询:
    cursor = conn.cursor()
    cursor.execute('select * from user')
    values = cursor.fetchall()
    print(values)


if __name__ == '__main__':
    connect()
