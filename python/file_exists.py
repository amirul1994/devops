path = 'test_file.txt'

import os

print(os.path.isfile(path))

import pathlib

file = pathlib.Path(path)

print(file.is_file())

print('-------------')
a = 'D:/test.txt'

import os

print(os.path.isfile(a))

import pathlib

b = pathlib.Path(a)
print(b.is_file())