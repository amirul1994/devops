def hello2(fname='amirul', lname='maula'):
    print(f"Full Name: {fname} {lname}")

hello2()
hello2('imam')

# Arbitrary Arguments
# def fun1(*args)

# Arbitrary Keyword Arguments
# def fun2(**kwargs)

def fun2(**kwargs):
    print(kwargs)
    print(kwargs['fname'])

fun2(fname='amirul', lname='maula', age='30')

print('-----------')
def flats(**kwargs):
    print(kwargs)
    print(kwargs['loc2'])

flats(loc1='shewrapara', loc2='jatrabari', loc3='matikata')

print('-----------------')

def hello3(*args, **kwargs):
    print(args, kwargs)

hello3('amirul', 'maula', 30, fname='amirul', lname='maula', age='30')
hello3('amirul', 'maula', 30)
hello3()

print('---------------')

def city(*args, **kwargs):
    print(args, kwargs)

city('dhaka', 'chattogram', city1='dhaka', city2='chattogram')
city('dhaka', 'chattogram')
city()