class city():
    def __init__(self, city1, city2):
        self.city1 = city1
        self.city2 = city2


name = city('dhaka', 'chattogram')

print(name.city1)
print(name.city2)

print('---------')

class person():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

a1 = person('amirul', 'imam')

print(a1)
print(a1.p1)
print(a1.p2)

print('--------')

class country():
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2

cn = country('bd', 'pl')

print(cn.c1)
print(cn.c2)

print('-----------')

class flat():
    def __init__(self, f1, f2, f3, f4):
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.f4 = f4

mother_flat = flat('shewrapara', 'jatrabari'
                   ,'matikata', 'matikata')

print(mother_flat.f1)
print(mother_flat.f2)
print(mother_flat.f3)
print(mother_flat.f4)

print('-----------')

class car():
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2

    def car_name(self):
        print('the first car is {}'.format(self.c1))


first = car('land rover', 'lamborghini')
print(first.c1)

first.car_name()

print('-------------------')

class planet():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def planet_name(self, p3):
        print('the name of our planet is {}'.format(self.p1))
        print('third planet is {}'.format(p3))

pn = planet('earth', 'mars')
print(pn.p1)
pn.planet_name('saturn')
