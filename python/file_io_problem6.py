# Write a Python program to copy the contents
# of a file to another file .

location = 'D:/file/t11.txt'
my_file = open(location, 'r')
read_file = my_file.read()

my_list = read_file.split()
print(my_list)

with open('D:/file/t12.txt', 'a') as file:
    for elements in my_list:
        file.write(elements + '\n')

with open('D:/file/t12.txt', 'r') as file:
    print(file.read())

print('---------')

import shutil

shutil.copyfile('D:/file/t1.txt', 'D:/file/t13.txt')

print(open('D:/file/t13.txt', 'r').read())

import shutil

shutil.copyfile('D:/file/t4.txt', 'D:/file/t14.txt')

a = open('D:/file/t14.txt', 'r')
print(a.readlines())