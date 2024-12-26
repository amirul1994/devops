class A:

    def __init__(self):
        print('from class a')

class B:

    def __init__(self):
        print('from class b')

class c(A, B):
    def __init__(self):
        print('from class c')
        A.__init__(self)
        B.__init__(self)

object_c = c()

