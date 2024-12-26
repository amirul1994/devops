class c1:
    def __init__(self, a):
        self.a = a

    def first(self):
        print(f'this is {self.a}')


class c2:
    def __init__(self, b):
        self.b = b

    def second(self):
        print(f'this is {self.b}')

class c3(c1, c2):
    def __init__(self, a, b, c):
        c1.__init__(self, a)
        c2.__init__(self, b)
        self.c = c

    def third(self):
        print(f'this is {self.c}')

obj = c3('land rover', 'bugatti', 'porsche')
obj.first()
obj.second()
obj.third()