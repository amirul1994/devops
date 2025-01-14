# Write a Python program to get a string made of the first 2 and last 2 characters of a given string. If the string length is less than 2, return the empty string instead.

a = 'd'

b = a[:2]
#print(b)

c = a[-2:]
#print(c)

if len(a) < 2:
    print("value can't be empty")
else:
    print(b+c)
