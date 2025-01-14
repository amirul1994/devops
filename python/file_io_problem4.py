# Write a Python program to count the frequency
# of words in a file.

all_line = open('D:/file/t8.txt', 'r')
all_line2 = all_line.read()

words = all_line2.split( )
print(words)

frequency = {}

for word in words:
    print(word)
    if word in frequency.keys():
        frequency[word] += 1
    else:
        frequency[word] = 1

print(frequency)
print('--------------')


# Write a Python program to get the file size of a plain file.

import os

print(os.path.getsize('D:/file/t3.txt'))