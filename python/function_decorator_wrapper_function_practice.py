def func1(L):
    def func2(mylist):
        print('this is the first line')
        L(mylist)
        print('this is the last line')

    return func2


mylist = [1, 2, 3, 4, 5]


def value(mylist):
    for i in mylist:
        print(i)


value = func1(value)
value(mylist)

print('-------------')


def letter(z):
    def func1():
        print('1')
        z()
        print('100')

    return func1

@letter
def letter2():
    for i in range(ord('A'), ord('E')+1):
        print(chr(i))

#letter2 = letter(letter2)
letter2()