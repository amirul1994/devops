import os

location = os.listdir('E:/Javascript')
print(location)

a = os.path.isfile('E:/Javascript')
b = os.path.isfile('E:/Javascript/subclass.html')

print(a)
print(b)

print('--------------------')

location2 = 'E:\Javascript'

total_files = os.listdir(location2)

for files in total_files:
    # print(os.path.join(location2, files))

    if os.path.isfile(os.path.join(location2, files)):
        print('{} is a file'.format(files))
    else:
        print('{} is a directory'.format(files))

print('*********************')

location3 = 'D:\ChatGPT Secrets Beginner to ChatGPT Ninja w 700+ Prompts'

all_files = os.listdir(location3)

for files2 in all_files:
    if os.path.isfile(os.path.join(location3, files2)):
        #print(files2, 'is a file')
        print('{} is a file'.format(files2))

    else:
        print('{} is a directory'.format(files2))
        #print(files2, 'is a directory')
