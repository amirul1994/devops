# Write a Python program to read last n lines of a file.

location = open('D:/file/t1.txt', 'r')

all_line = location.readlines()

#print(len(all_line))

n = -1

while n >= -3:
    print(all_line[n])
    #print(n)
    n -= 1

print('--------------')

# Write a Python program to read a file line by line
# and store it into a list.
# and count number of lines

location2 = open('D:/file/t8.txt', 'r')

all_line2 = location2.readlines()

my_list = []

n = 0
while n < len(all_line2):
    my_list.append(all_line2[n])
    n += 1

print(my_list)
print('number of lines is {}'.format(len(my_list)))
print(type(my_list[0]))

import os

location3 = os.scandir('D:/file')

for files in location3:
    print(files)
    if files.is_file():
        print(files)