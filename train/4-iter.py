#!/usr/bin/python3
# 文件名: 4-iter.py

import sys

# 迭代器(iter)、生成器


# ----------生成器----------------
"""
在 Python 中，使用了 yield 的函数被称为生成器（generator）。
跟普通函数不同的是，生成器是一个返回迭代器的函数，只能用于迭代操作，更简单点理解生成器就是一个迭代器。
"""


def fibonacci(n):
    a, b, count = 0, 1, 0
    while True:
        if count > n:
            break
        yield a  # 实际上就相当于每次都把a的值放到集合里面 最后返回一个集合出去
        a, b = b, a + b
        count += 1


if __name__ == '__main__':
    f = fibonacci(5)
    print(f)
    print(sys.api_version)

    it = iter((1, 2, 3, 4))
    while True:
        try:
            print(next(f))
        except:
            pass
