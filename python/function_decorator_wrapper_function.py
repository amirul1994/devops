# wrapper function

def myWrapper(fn):
    def test():
        print('i am from test! before')
        fn()
        print('i am from test! after')

    return test

@myWrapper
def greet():
    print('hello world')
@myWrapper
def hello():
    print('hello hello')

#greet = myWrapper(greet)
greet()

print('--------')

#hello = myWrapper(hello)
hello()

print('-----------')
