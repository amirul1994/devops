def my_func():
    print('hello world')

def print_function(func):
    func()
    print('this is from print function')

print_function(my_func)

print('------------')

# nested function
def greet(name):

    def hello():
        return 'hello my name is ' + name

    return hello

my_variable = greet('amirul')
print(my_variable())

print('----------')

def greet(func):
    def inner():
        func()
        print('this is from inner function')
    return inner
@greet
def hello():
    print('this is from hello function')

print(hello())