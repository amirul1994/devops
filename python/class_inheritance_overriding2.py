class A:
    def __init__(self, name):
        self.name = name

    def hello(self):
        print('hello from class A')

class B(A):
    pass

obj = B('amirul')
obj.hello()


print('---------')

class Car:
    def __init__(self, c1):
        self.c1 = c1

    def two(self):
        print(self.c1)
        print('the car names are printed above')

class Car2(Car):
    print('bugatti')
    pass


opt = Car2('Land Rover')
opt.two()

print('------------')

class C:
    def __init__(self, name):
        self.name = name

    def hello(self):
        print('hello from class A')

class D(C):
    def __init__(self):
        pass

    def hello(self):
        print('hello from class D')

obj2 = D()
obj2.hello()

print('------------')

class first:
    def __init__(self, a):
        self.a = a

class two(first):
    def __init__(self):
        print('1')
        pass

obj3 = two()