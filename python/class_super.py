class A:
    def __init__(self):
        print('from class a')

class B(A):
    def __init__(self):
        print('from class b')
        A.__init__(self)

    def my_method(self):
        print('this is from class b')

class C(B):

    def __init__(self):
        print('from class c')
        # for multiple inheritance python
        # follows MRO(method resolution order)
        super().__init__()

    def my_method(self):
        print('this is from class c')

class D(C, B):
    def __init__(self):
        print('from class d')
        super().__init__()

object_d = D()

