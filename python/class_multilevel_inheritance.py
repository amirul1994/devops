class A:

    def __init__(self):
        print("from class A")

class B(A):

    def __init__(self):
        print('from class B')
        A.__init__(self)

class C(B):
    def __init__(self):
        print('from class c')
        B.__init__(self)


object_c = C()


print('-------------')


class one:
    def __init__(self, a):
        self.a = a
        print(self.a)



class two(one):
    def __init__(self, a, b):
        self.b = b
        print(self.b)
        one.__init__(self, a)

class three(two):
    def __init__(self, a, b, c):
        self.c = c
        print(self.c)
        two.__init__(self, a, b)


obj2 = three(1, 2, 3)