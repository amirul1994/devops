# Write a Python program to read first n lines of a file.

location = open('D:/file/t1.txt', 'r')

n = 1

while n <= 4:
    print(location.readline())
    n += 1

print('---------')

# Write a Python program to append text to a file and display the text.

location2 = open('D:/file/t1.txt', 'a')
location2.write('\nEnd2')
location3 = open('D:/file/t1.txt', 'r')
print(location3.read())