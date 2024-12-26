l = [1, 3, 4, 6, 88, 4, 2, 9, 5]

def func(n):
    return n%2==1

newList = filter(func, l)

newList2 = list(filter(func, l))

print(newList)
print(newList2)

print('--------------')


mylist = ['1', '2']

def find_one():
    for i in mylist:
        if i == 1:
            return i

result = print(filter(find_one, mylist))
