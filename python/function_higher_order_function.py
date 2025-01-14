# higher order function accepts another
# function as an argument

def hof(fn):
    print(fn.__name__)
    fn()

def greet():
    print('hello world')

def hello():
    print('hello bohubrihi')

# hof('amirul')
#hof(hello)
#hof(greet)

print('----------')

li = [1, 2, 3, 4, 5, 6]

def myFilter(fn, l):
    newL = []

    for i in l:
        if fn(i):
            newL.append(i)
    return newL

#newList = list(filter(lambda x: x%2==1, li))
newList = myFilter(lambda x: x%2==1, li)
print(newList)