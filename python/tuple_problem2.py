# Write a Python program to create the colon of a tuple.

from copy import deepcopy

# It looks like you've imported the deepcopy function
# from the copy module in Python.
# deepcopy is a function used to create a deep copy of objects,
# meaning it creates a new object that is a copy
# of the original object,
# and all of its nested objects, recursively.

a = 1, 2, 3, 4, 5, []
b = deepcopy(a)
print(b)

print(id(a))
print(id(b))

b = b + (6,)
print(id(b))
print(id(a))

a[5].append(7)
print(a)

b[5].append(7)
print(b)