# 元组(tuple)、字典（dict）

if __name__ == '__main__':
    tup = ()
    tup1 = (1, 2, 3, 'huang')
    tup2 = (1,)  # 当元组只有一个元素的时候，需要加逗号，否则括号会被当作运算符使用
    print(tup2)

    dict1 = {}
    dict2 = {1: 'huang', 2: 'zhao', 'hh': 23}
    print(dict2['hh'])

    s = dict2.values()
    print(s)
    key = dict2.keys()
    print(key)
    # dict2.clear()
