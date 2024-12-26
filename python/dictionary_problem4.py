# Write a Python script to merge two Python dictionaries.

dictionary1 = {'a': 1, 'c': 2, 'd': 3}
dictionary2 = {'e': 4, 'f': 5}

item1 = dictionary1.items()
item2 = dictionary2.items()

item1 = tuple(item1)
item2 = tuple(item2)

dictionary3 = item1 + item2
dictionary3 = dict(dictionary3)
print(dictionary3)

print('----------')

dictionary1.update(dictionary2)
print(dictionary1)

print('--------')

# Write a Python program to iterate
# over dictionaries using for loops.

for a,b in dictionary3.items():
    print(a,b)

print('-----------')

# Write a Python program to sum all the items in a dictionary.

value = dictionary3.values()
print(value)

sum = 0
multiplication = 1

for i in value:
    sum += i
    multiplication *= i

print(sum)
print(multiplication)