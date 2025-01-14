# reduce() is used to process all the elements
# of an iterable ,and return a single result

from functools import reduce

li = [1, 2, 3, 4, 2, 3, 4]

def func(x, y):
    print(x, y)
    return x + y

sum = reduce(func, li)
print(sum)