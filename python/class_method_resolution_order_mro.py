class A:
    def __init__(self, name):
        self.name = name

    def hello(self):
        print('hello from class A')

class B:
    def __init__(self, job):
        self.job = job

    def hello(self):
        print('hello from class B')

class C(B, A):
    def __init__(self):
      pass

    def hello(self):
        print('hello from class C')

obj = C()
obj.hello()
print(C.__mro__)
