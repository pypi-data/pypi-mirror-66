class DecoratorClass:
    def __init__(self, original):
        self.original = original

    def __call__(self, *args, **kwargs):
        print('{} 함수가 호출되기전입니다.'.format(self.original.__name__))
        return self.original(*args, **kwargs)


@DecoratorClass
def display():
    print('display함수가 실행되었습니다')


@DecoratorClass
def display_info(*args, **kwargs):
    for i in args:
        print('cur : ', i)

    for i in kwargs:
        print('kwargs : ', i, kwargs[i])


display()
print()
display_info('goodgood', 'nogood', 'badbad', 28, ww=25)
