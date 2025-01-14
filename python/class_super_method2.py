class A:
    def __init__(self, name):
        self.name = name

    def hello(self):
        print('hello from class A')

class B(A):
    def __init__(self, name, job):
        super().__init__(name)
        self.job = job

    def hello(self):
        print(f'{self.name} is a {self.job}')


obj = B('amirul', 'devops')
obj.hello()

print('--------------')

class one:
    def __init__(self, s1):
        self.s1 = s1
        print(f'{self.s1} students in class one')

class two(one):
    def __init__(self,s1,s2):
        super().__init__(s1)
        self.s2 = s2
        print(f'{self.s2} students in class two')

third = two('20', '30')
