# Write a Python program to count the elements in a
# list until an element is a tuple.

my_list = ['imam', 'muhammad', 'amirul', [], (1, 2), {}]
num_o_element = 0

for i in my_list:
    # print(type(i))

    if isinstance(i, tuple):
        print(i)
        print(num_o_element)

    num_o_element += 1

print('-----------')

# Write a Python program to convert a given tuple of positive integers into an integer.
# Original tuple:
# (1, 2, 3)
# Convert the said tuple of positive integers into an integer:
# 123
# Original tuple:
# (10, 20, 40, 5, 70)
# Convert the said tuple of positive integers into an integer:
# 102040570

tup = (1, 2, 3, -4)
my_list = []

for i in tup:
    if i > 0:
        my_list.append(str(i))

print(my_list)

str = ''.join(my_list)

result = int(str)
print(type(result))