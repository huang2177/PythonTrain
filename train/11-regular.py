# 正则表达式
# re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；
# re.search匹配整个字符串，直到找到一个匹配
import re

text = '<p><div>黄</div></p>'

pattern = r'<(\w+)><(\w+)>\w+</\2></\1>'
print(re.match(pattern, text))


def fn(match):
    return str(int(match.group()) - 10)


string = 'Kobe今年39岁了'
pattern1 = re.compile(r'\d+')
sub = pattern1.sub(fn, string)
print(sub)
