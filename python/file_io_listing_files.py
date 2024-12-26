import os

location = '../folder'
all_files = os.listdir(location)

for files in all_files:
    # isfile() will check whether there is file or not
    if os.path.isfile(os.path.join(location, files)):
        print('{} is a file'.format(files))


print('-----------')

all_files = os.scandir(location)

for file in all_files:

    if file.is_file():
        print("{} is a file".format(file.name))

print('--------------')

import pathlib

location_object = pathlib.Path(location)

for file in location_object.iterdir():
    print(file)

print('--------------')

for file in location_object.iterdir():
    if file.is_file():
        print(file.name)