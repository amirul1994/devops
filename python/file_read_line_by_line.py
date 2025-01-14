file = open('test_file.txt', 'r')

print(file.readline())
print(file.readline())
print(file.readline())

while True:
    line = file.readline()
    if not line:
        break
    print(line)


all_files = file.readlines()
print(all_files)