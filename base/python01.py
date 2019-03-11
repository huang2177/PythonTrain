"""
列表List
"""

if __name__ == '__main__':
    _list = [1, 3, 4, 'huang', 'zhao']

    # list的取值
    print(_list[0])
    # 切片取出_list的1~4的元素（不包括4的元素）
    print(_list[1:4])

    # list的更新
    _list.append(5)
    _list.extend((23, 3))  # 在列表末尾追加另一个序列中元素
    print(_list)

    # list的删除
    a = _list.pop(2)
    del _list[2]
    _list.remove('huang')

    #
    ll = [l for l in _list]

    # 用特定字符来连接一个集合
    print("&".join(_list))
