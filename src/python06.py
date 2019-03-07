import os

if __name__ == '__main__':
    with open('D:/test.txt', 'w') as f:
        f.write("写入文本！！")

    with open('D:/test.txt', 'r') as f:
        txt = f.readline()
        print(txt)

    print(os.getcwd())
    print(os.access('D:/', os.F_OK))
