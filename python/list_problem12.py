# Write a Python program to calculate the
# difference between the two lists.

a = [1, 2, 3, 4, 5, 8, 10]
b = [4, 5, 6, 7, 8, 9]

c = a[:]
d = b[:]

for i in a:
    if i in b:
        print(i)
        c.remove(i)
        d.remove(i)

print(c)
print(d)

print(c+d)
print('--------')
c.extend(d)
print('the new list with the differences: {}'.format(c))

print('---------')

diff1 = list(set(a) - set(b))
diff2 = list(set(b) - set(a))

total_diff = diff1 + diff2
print(total_diff)