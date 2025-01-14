# Write a Python program to unzip a list of
# tuples into individual lists.

my_list = [(1, 'a'), (2, 'b'), (3, 'c')]

list1 = []
list2 = []

for x, y in my_list:
    list1.append(x)
    list2.append(y)

print(list1)
print(list2)

print('--------------')

# Write a Python program to reverse a tuple.

tup = (1, 2, 3, 4, 5, 6, 7)

tup = list(tup)

tup.reverse()

print(tuple(tup))