import os

path = '../new_folder'

# path.exists() for checking existence of directory
if os.path.exists(path):
    os.removedirs(path)