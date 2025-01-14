# Write a Python program to reverse a string.

def func3(n):
    def func5():
        print('the reverse string is: ')
        print(n())

    return func5

def func4():
    user_input = '1234'
    output = []

    n = -len(user_input)

    for i in range(-1, n-1, -1):
        #print(user_input[i])
        output.append(user_input[i])

    #print(output)

    output2 = ''.join(output)

    return output2

func4 = func3(func4)
func4()

print('--------------')

def func3(n):
    def func5():
        print('the reverse string is: ')
        print(n())

    return func5

@func3
def func4():
    user_input = 'abcd'
    output = []

    n = -len(user_input)

    for i in range(-1, n-1, -1):
        #print(user_input[i])
        output.append(user_input[i])

    #print(output)

    output2 = ''.join(output)

    return output2

func4()