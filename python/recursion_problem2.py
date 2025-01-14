# Write a Python program to convert an integer to a string in
# any base.
'''
a = '12'
b = int(a, 8)
print(b)

c = '16'
d = bin(int(c))
print(d)

print('----------------')
'''


def convert(a, b):
    value = '0123456789ABCDEF'
    if a < b:
        return value[a]
    else:
        return convert(a//b, b) + value[a%b]

print(convert(1,2))