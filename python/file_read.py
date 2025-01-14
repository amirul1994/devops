# open() will open the file and return as object

file = open('test_file.txt', 'r')

print(file.read())

print('++++++++')

open('test_file.txt', 'r')


file = open('test_file.txt', 'r')


print(file.read())

print('--------')

print(open('D:/test.txt', 'r'))

file = open('D:/test.txt', 'r')

print(file.read())

print('***********')

file2 = open('D:/test.txt', 'r')
print(file2.read())