# 集合 set（不重复）

if __name__ == '__main__':
    s = {1, 3, 5, 'huang'}
    s.add('jiojdci')

    s.remove('huang')  # 移除 如果不存在会报错
    s.discard('huang')  # 移除 不会报错

