# Write a python program to find the longest words.

line = open('D:/file/t8.txt', 'r').read()
print(line)
print(type(line))

line2 = line.split( )
print(line2)

print('the longest word in the file is "{}"'.format(max(line2)))