# Write a Python program to write a list to a file.

my_list = ['imam', 'muhammad', 'amirul', 'maula']

n = 0

while n < len(my_list):
    new_file = open('D:/file/t9.txt', 'a')
    new_file.write(my_list[n] + '\n')
    n += 1

print(open('D:/file/t9.txt', 'r').read())

print('----------')

# the following solution is the more
# appropriate solution in python

my_list2 = ['imam', 'muhammad', 'amirul', 'maula']

with open('D:/file/t10.txt', 'a') as my_file:
    for item in my_list2:
        my_file.write(item + '\n')

with open('D:/file/t10.txt', 'r') as my_file2:
    print(my_file2.read())

print('-------------')

my_list3 = ['chattogram', 'dhaka', 'rajshahi', 'khulna']

with open('D:/file/t11.txt', 'a') as file:
    for elements in my_list3:
        file.write(elements + '\n')

with open('D:/file/t11.txt', 'r') as file:
    print(file.read())