class opt:
    def __init__(self, a):
        self.a = a

    name = 'amirul'

    @classmethod
    def c1(cls):
        print('my name is {}'.format(cls.name))

opt.c1()

print('-----------')

class two:
    def __init__(self, b):
        self.b = b

    @staticmethod
    def age():
        print('my age is 30')


second = two('shewrapara')
print(second.b)

two.age()