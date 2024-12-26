# The map() function in Python is a built-in function
# that applies a given function to each item
# of an iterable (such as list, tuple, etc.)
# and returns a list of the results.

def func(n):
    return n*n*n

l = [3, 4, 1, 0, 6]

newL = map(func, l)
# newL = [n*n*n for n in l]

newL2 = list(map(func, l))
newL3 = tuple(map(func, l))
newL4 = set(map(func, l))

print(newL)
print(newL2)
print(newL3)
print(newL4)

print('-----------')

l2 = ['amirul', 'amirulcorp', 'chattogram']

l3 = list(map(list, l2))
print(l3)

print('-----------')