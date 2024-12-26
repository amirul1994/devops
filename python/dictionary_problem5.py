# Write a Python program to map two lists into a dictionary.

keys = ['red', 'green', 'blue']
values = ['#FF0000','#008000', '#0000FF']

my_list = []
n = 0

while n < len(values):
    for i in keys:
        my_list.append((i, values[n]))
        n += 1

# print(my_list)

my_dictionary = dict(my_list)
print(my_dictionary)

print('---------')

my_dictionary2 = dict(zip(keys, values))
print(my_dictionary2)