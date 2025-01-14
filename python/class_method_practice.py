
class Car:
    other = 'discovery sport'

    def __init__(self, a, b):
        self.name = a
        self.brand = b

    @classmethod
    def car3(cls):
        return cls.other


car1 = Car('range rover evoque', 'land rover')
car2 = Car('defender 130', 'land rover')

print(Car.car3())


print('++++++++++++++')
class sc:
    def __init__(self, a, b ):
        self.name = a
        self.brand = b

    new = "mclaren"

    @classmethod
    def nc(cls, c):
        print(c)

        return cls.new


c1 = sc('bugatti mistral', 'bugatti')
print(c1.name)

print(sc.nc('mclaren 570gt'))


print('----------------')

class veg:
    def __init__(self, a, b):
        self.first = a
        self.second = b

    new_veg = 'raddish'

    @classmethod
    def other(cls, c):
        print(c)
        return cls.new_veg

veg1 = veg('potato', 'carrot')
veg2 = veg('cabbage', 'papaya')

print(veg1.first)
print(veg2.second)

veg.other('pumpkin')


print('-----------------')

class Person:

    def __init__(self, a, b):
        self.name = a
        self.age = b

    def address(self, c):
        return 'the name is {}, address is {}'.format(
            self.name, c)

    @classmethod
    def job(cls, d):
        return 'the job is {}'.format(d)


obj1 = Person('amirul', 30)

print(obj1.address('shewrapara'))
print(Person.job('nil'))


