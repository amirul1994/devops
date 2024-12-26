# Write a Python program to assess if a
# file is closed or not.

open_file = open('D:/file/t1.txt', 'r')
read_file = open_file.readline()
#read_file.close()
open_file.close()

print('-------------')

# Write a Python program that takes a text file as input and
# returns the number of words of a given text file.
# Note: Some words can be separated by a comma with no space.

def word_count(file_path):
    open_file = open(file_path, 'r')
    read_file = open_file.read()

    read_file2 = read_file.replace(',', ' ')

    my_list = read_file2.split()

    return 'number of words: {}'.format(len(my_list))


print(word_count('D:/file/t5.txt'))
print(word_count('D:/file/t11.txt'))
print(word_count('D:/file/t1.txt'))