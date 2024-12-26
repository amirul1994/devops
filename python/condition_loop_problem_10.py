#  Write a Python program that accepts a sequence of comma separated
#  4 digit binary numbers as its input.
#  The program will print the numbers that are divisible by 5 in a comma separated sequence.


a = '0100', '0011', '1010', '1001', '1100', '1001', '0101'
b = []

i = 0

while i < len(a):
    c = int(a[i], 2)
    #print(c)

    if c % 5 == 0:
        print(c)
        print(a[i])
        print('****')
        b.append(a[i])

    i += 1

print(b)

print('****')
d =','.join(b)

print(d)

print(type(d))