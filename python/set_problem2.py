# Write a Python program to create an intersection of sets.
a = {1, 2, 3}
b = {3, 4, 5}

print(a & b)

# Write a Python program to create set difference.
a = {1, 2, 3}
b = {3, 4, 5}

n = a.difference(b)
print(n)

o = b.difference(a)
print(o)

# Write a Python program to create a shallow copy of sets.
c = {1, 2, 4}
m = c.copy()
print(m)
print(id(c))
print(id(m))

g = [1,2,3]
h = g.copy()
print(h)

'''
i = (1, 2, 3)
j = i.copy()
print(j)
'''

"""
i = '1234'
j = i.copy()
print(j)
"""

# Write a Python program to find the maximum and minimum values in a set.
d = {1, 2, 3, 4, 5, 6, 100}
print(min(d))
print(max(d))