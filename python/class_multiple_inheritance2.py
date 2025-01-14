class first:
    def __init__(self, a):
        self.a = a

    def op1(self):
        print(f'this is {self.a}')

class second:
    def __init__(self, b):
        self.b = b

    def op2(self):
        print(f'this is {self.b}')


class third(first, second):
    def __init__(self, a, b, c):
        #super().__init__(a)
        #super().__init__(b)
        first.__init__(self, a)
        second.__init__(self, b)
        self.c = c

    def op3(self):
        print(f'this is {self.c}')

obj = third('first', 'second', 'third')
obj.op1()
obj.op2()
obj.op3()