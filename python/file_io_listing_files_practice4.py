import pathlib

location = 'D:\Installed Software'

print(pathlib.Path(location))

print('----------')

a = pathlib.Path(location)

b = pathlib.Path(location).iterdir()

print(b)

print('---------------')

for c in b:
    print(c)

print('---------------')