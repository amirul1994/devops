# Write a Python program to convert temperatures to and from Celsius and Fahrenheit.

def celsius():
    f = int(input('enter the value in fahrenheit: '))
    c = round((5 * (f-32)/9), 2)

    print ('the value in celsius is {}'.format(c))

celsius()

print('--------------')
def fahrenheit():
    c = int(input('enter the value in celsius: '))

    f = str(round(((9*c)/5)+32, 2))

    print('the value in fahrenheit is ' + f)

fahrenheit()