class first:
    def __init__(self, a):
        self.a = a

    def show(self):
        print(f'the first value is {self.a}')


class two(first):
    def __init__(self, a, b):
        super().__init__(a)
        self.b = b

    def show2(self):
        print(f'the second value is {self.b}')


values = two(50, 60)
values.show()
values.show2()