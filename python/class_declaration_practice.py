class Car:
    def __init__(self):
        self.brand = 'ferarri'
        self.date = '20-07-2004'

a = Car()

print(a.brand)
print(a.date)

print('-----------')
class Flat:
    def __init__(self, a, b, c, d):
        self.first = a
        self.second = b
        self.third = c
        self.fourth = d

home = Flat('shewrapara', 'jatrabari', 'matikata', 'matikata')

print(home)
print(home.first)
print(home.second)
print(home.third)
print(home.fourth)

print('-----------')
class Sister():
    def __init__(self, f, g):
        self.name = f
        self.age = g

obj1 = Sister('raisa', '26')

print(obj1.name)
print(obj1.age)


print('++++++++++++++++')

class country:

    def __init__(self, a, b, c):
        self.country_name = a
        self.capital = b
        self.area = c

    def cn_name(self):
        return 'the name of the country is {}'.format(self.country_name)
        #print('the name of the country is {}'.format(
# self.country_name))


cn1 = country('bangladesh', 'dhaka', '147k')
cn2 = country('india', 'delhi', '3200k')

print(cn1.country_name)

print(cn1.cn_name())
print(cn2.cn_name())










































