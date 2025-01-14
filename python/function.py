def greeting(a):
    print('hello', a)

greeting('amirul')

def username(firstname, lastname):
    print("first name is {}".format(firstname))
    print("last name is {}".format(lastname))
    print("full name is {} {}".format(firstname, lastname))

username('imam muhammad', 'amirul maula')
username(firstname = 'renesa bente', lastname = 'maula' )

def calculate_net_price(total_price = 100, tax_percent=5):
    net_price = total_price + total_price * (tax_percent / 100)
    print(net_price)

calculate_net_price()
calculate_net_price(120)

'''
def square(a):
    return a ** 2
'''

def cube(a):
    return a**3

'''
def average(a, b):
    return (a+b)/2
'''

# lambda function is a function without name
# also known as anonymous function
# can take any number of arguments,
# but can only have one expression
# 'lambda arguments : expression'

square = lambda a : a ** 2
print(square(2))

average = lambda a, b : (a+b)/2
print(average(4,6))
