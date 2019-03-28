import socket
from mysql import connector


def get_user():
    conn = connector.connect(user='root', password='root', database='huang', use_unicode=True)
    # 运行查询:
    cursor = conn.cursor()
    cursor.execute('select * from students')
    values = cursor.fetchall()

    with open('user.html', 'r', encoding='utf-8') as f:
        html = f.read()

    trs = ''
    for value in values:
        ths = ''
        for v in value:
            ths += f'\t<td>{v}</td>\n'
        trs += f'<tr>\n{ths}</tr>'

    return html.replace('content', trs)


def main():
    sock = socket.socket()
    sock.bind(('127.0.0.1', 11111))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        headers, body = data.decode().split('\r\n\r\n')
        method, url, protocol = headers.split('\r\n')[0].split(' ')

        conn.send(b'Http/1.1 200 OK\r\n\r\n')
        conn.send(parse_url(url))
        conn.close()


def parse_url(url):
    if url in routers.keys():
        return bytes(routers[url](), encoding='utf-8')
    else:
        return b'404 not found!'


if __name__ == '__main__':
    routers = {'/user.html': get_user}
    main()
