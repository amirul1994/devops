import os
print (os.scandir('D:\AI Python\AI Python'))

print('----------')

a = os.scandir('D:\AI Python\AI Python')

for b in a:
    print(b)

print('****************')

c = ('D:\AI Python\AI Python')
print('------------')

'''
The is_file() method is a part of the DirEntry object returned 
by os.scandir(). It is used to check whether 
the item represented by the DirEntry is a regular file. 
'''

location = os.scandir('D:\AI Python\AI Python')

for files in location:
    print(files)
    print('*****************')
    if files.is_file():
        print(files, 'is a file')
        print('*****************')
        print('{} is a file'.format(files))
    else:
        print('{} is a directory'.format(files))
