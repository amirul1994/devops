# Write a Python program to get a single string from
# two given strings, separated by a space and
# swap the first two characters of each string.

a = 'abcde'
b = 'vwxyz'

c = b[0:2] + a[2:]
print(c)

d = a[0:2] + b[2:]
print(d)

e = "{} {}".format(c, d)
print(e)

print(b[0:2] + a[2:] + ' ' + a[0:2] + b[2:])