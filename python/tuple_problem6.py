# Write a Python program to replace the last value of tuples in a list.

my_list = [(10, 20, 40), (40, 50, 60), (70, 80, 90)]

index_number = 0

for i in my_list:
    if index_number == len(my_list) - 1:
        my_list[index_number] = (70, 80, 100)
    index_number += 1

print(my_list)

print('------------')

# Write a Python program to remove an empty
# tuple(s) from a list of tuples.

my_list2 = [(), (), ('',), ('a', 'b'), ('a', 'b', 'c'), ('d')]

i = len(my_list2) - 1

while i >= 0:
    if my_list2[i] == ():
        my_list2.pop(i)

    i -= 1

print(my_list2)