# Write a Python program to find the highest 3 values of
# corresponding keys in a dictionary.

my_dict = {'a': 34,
           'b': 26,
           'c': 29,
           'd': 24,
           'e': 56,
           'f': 12}

value = list(my_dict.values())
print(value)

value = sorted(value)
print(value)

value.reverse()
print(value)

n = 0

while n <= 2:
    print(value[n])
    n += 1