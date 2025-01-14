def addition(a):
    return a+10

mylist = [1, 2, 3, 4]

result = list(map(addition, mylist))
print(result)