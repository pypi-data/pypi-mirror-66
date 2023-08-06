# -*- coding: utf-8 -*-
# 클로저 예제


def html_tag(tag):
    def wrap_text(msg):
        print('<{0}>{1}<{0}>'.format(tag, msg))

    return wrap_text


print_h1 = html_tag('h1')
print(print_h1)  # 함수 오브젝트출력
print_h1('첫 번째 테스트')
print_h1('두 번째 테스트')
print(dir(print_h1))
print()
print(type(print_h1.__closure__))
print()
print(print_h1.__closure__)
print()
print(print_h1.__closure__[0])
print()
print(dir(print_h1.__closure__[0]))
print()
print(print_h1.__closure__[0].cell_contents)
