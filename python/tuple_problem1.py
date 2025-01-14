# Write a Python program to create a tuple with different data types.

a = (['asd', 'ffg'], {'adsad', 'asdasdad'}, {'name': 'amirul',
                                             'age': 30})
print(a[2]['age'])
print(type(a[1]))
print(type(a[2]))

print('-------------')

# Write a Python program to create a tuple of
# numbers and print one item.

tup1 = (1, 2, 3, 4, 5, 6)
print(type(tup1))
print(tup1[3])

print('----------')

# Write a Python program to unpack a tuple into several variables.

tup2 = (1, 2, 3)

a1, a2, a3 = tup2
print(a1)
print(a2)
print(a3)

print('------------')
b = [1, 2, 3]
b1, b2, b3 = b
print(b1)
print(b2)
print(b3)

print('-------------')

s = {1, 2, 3}
s1, s2, s3 = s
print(s1)
print(s2)
print(s3)

print(s2)

str = "imam"
str1, str2, str3, str4 = str
print(str1)
print(str2)
print(str3)
print(str4)

print('---------')

dict = {'name': 'amirul', 'age': 30}
dict1, dict2 = dict
print(dict1)
print(dict2)

print('-----------')

tup3 = 'imam', 'muhammad', 'amirul'
tup3 = tup3 + ('maula',)
print(tup3)

print('---------------')

tup4 = 1, 2, 3
tup4 = tup4 + (4,)
print(tup4)

print('------------')

# Write a Python program to add an item to a tuple.
tup5 = ('iman', 'land', 'car', 'flat', 'farm', 'economy',
        'natural resource')
tup5 = list(tup5)
print(tup5)

tup5.append('military')

tup5 = tuple(tup5)
print(tup5)

print('-------')

# Write a Python program to convert a tuple to a string.
tup6 = 'i', 'm', 'a', 'm'
str = "".join(tup6)
print(str)

# Write a Python program to get the 4th element from the last element of a tuple.
tup7 = 'chattogram', 'dhaka', 'khulna', 'barisal', 'rajshahi'
print(tup7[-4])