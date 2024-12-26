from functools import reduce
def multi(a, b):
    return a * b

mylist = [1, 2, 3, 4]

result = reduce(multi, mylist)
print(result)