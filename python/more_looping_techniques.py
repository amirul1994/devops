myList = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']

# 'enumerate() will iterate the list with item and index number'

for fruit in enumerate(myList):
    print(fruit)


print('----------')

myList2 = ['apple', 'orange', 'apple', 'pear', 'orange',
           'banana']

for i,fruit in enumerate(myList2):
    print(f'{i} index of {fruit}')

print('-------------')

# zip()
myList3 = ['apple', 'orange', 'apple', 'pear', 'orange',
           'banana']
myList4 = [1, 2, 3, 4, 5, 6]

for i in zip(myList3, myList4):
    print(i)

print('-------------')

for i,j in zip(myList3, myList4):
    print(i, j)

print('-------------------')

for i in sorted(myList):
    print(i)

print('----------')

for i in reversed(sorted(myList)):
    print(i)