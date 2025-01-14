def number(n):
    print(n.__name__)
    return n()

def number2():
    n = 1

    while n <= 10:
        print(n)
        n += 1


number(number2)