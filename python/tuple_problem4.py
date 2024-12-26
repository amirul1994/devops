# Write a Python program to convert a tuple to a dictionary.

tup = ((2, 'a'), (3, 'b'), (4, 'd'))
print(dict((y, x) for x, y in tup))

print('--------------')

tup2 = (('a', 2), ('b', 3), ('d', 4))
print(dict((y,x) for x, y in tup2))

print('-------------')
for x, y in tup:
    print(x)