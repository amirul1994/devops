a = []

while True:
    b = input("enter a line or terminate: ")

    if not b:
        break

    else:
        a.append(b)

for c in a:
    print(c.lower())

print('---------------')

lines = []

if lines == []:
    b = input('enter lines or terminate: ')

    if b != '':
        lines.append(b)


for line in lines:
    print(line.lower())





