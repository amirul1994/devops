# Write a Python program to print the numbers of a
# specified list after removing even numbers from it.

my_list = [1, 2, 3, 4, 5]

for i in my_list:
    if i % 2 == 0 :
        my_list.remove(i)

print(my_list)

print('***************')

def odd_list(my_list):
    j = 0
    index_number = 0

    for i in my_list:
        #print(i, index_number)
        if i % 2 == 0:
            my_list.pop(index_number)
        index_number += 1

    print(my_list)

odd_list([1, 2, 3, 4, 5])