# Write a Python function to multiply all the numbers in a list.

from functools import reduce

my_tup = (8, 2, 3, -1, 7)

def mul(a, b):
    multi = 1
    for i in my_tup:
        multi *= i

    return multi

result = reduce(mul, my_tup)
print(int(result))

print('---------')


# Write a Python function
# to calculate the factorial of a number

def func1(fact):
    print('the factorial is: ')
    fact()

def value():
    factorial = 1
    n = 5

    while n > 0:

        factorial *= n
        n -= 1

    print (factorial)


result = func1(value)
