import os

print(os.scandir('D:\Installed Software'))
print('-------------')

path = os.scandir('D:\Installed Software')

for item in path:
    print(item)

print('--------------')

path = os.scandir('D:\Installed Software')
for item in path:
    if (item.is_file()):
        print('{} is a file'.format(item))
    else:
        print(item, 'is a directory')