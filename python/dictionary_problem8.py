# Write a Python program to combine two dictionary
# by adding values for common keys.
# d1 = {'a': 100, 'b': 200, 'c':300}
# d2 = {'a': 300, 'b': 200, 'd':400}
# Sample output: Counter({'a': 400, 'b': 400, 'd': 400, 'c': 300})

d1 = {'a': 100, 'b': 200, 'c':300, 'e': 400}
d2 = {'a': 300, 'e': 250, 'b': 200, 'd':400}

tup1 = d1.items()
tup2 = d2.items()

key1 = list(d1.keys())
key2 = list(d2.keys())

print(key1)
print(key2)

d3 = {}

for i in key1:
    if i in key2:
        # print(i)
        d3[i] = d1[i] + d2[i]

print(d3)

d1.update(d3)
print(d1)