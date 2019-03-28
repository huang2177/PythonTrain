import socket

from jinja2 import Template
from mysql import connector
from mysql.connector.cursor_cext import CMySQLCursorDict


def get_teachers():
    conn = connector.connect(user='root', password='root', database='huang', use_unicode=True)
    cursor = conn.cursor(CMySQLCursorDict)
    cursor.execute('SELECT * FROM teachers')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return generate_template(data)


def generate_template(data):
    with open('teacher.html', 'r', encoding='utf-8') as f:
        html = f.read()
    template = Template(html)
    html = template.render(data=data)
    print(html)
    return html


def parse_url(url):
    if url in routers.keys():
        return bytes(routers[url](), encoding='utf-8')
    else:
        return b'404 not found!'


def main():
    sock = socket.socket()
    sock.bind(('127.0.0.1', 11111))
    sock.listen(5)

    while True:
        conn = sock.accept()[0]
        data = conn.recv(1024)

        headers, body = data.decode().split('\r\n\r\n')
        method, url, protocol = headers.split('\r\n')[0].split(' ')

        conn.send(b'Http/1.1 200 OK\r\n\r\n')
        conn.send(parse_url(url))
        conn.close()


if __name__ == '__main__':
    routers = {'/teacher.html': get_teachers}
    main()
