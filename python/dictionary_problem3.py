# Write a Python script to generate and print a dictionary
# that contains a number (between 1 and n) in the form (x, x*x).
# Sample Dictionary ( n = 5) :
# Expected Output : {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

def sqr(n):
    my_list = []

    while n >= 1:
        my_list.append((n, n*n))
        # my_list.append({n, n * n})
        # print(my_list)
        n -= 1

    print(my_list)

    my_list.reverse()

    print(my_list)

    my_list = dict(my_list)
    print(my_list)

sqr(5)

print('----------')
# Write a Python script to print a dictionary where
# the keys are numbers between 1 and 15 (both included) and
# the values are the square of the keys.
# Sample Dictionary
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81,
# 10: 100, 11: 121, 12: 144, 13: 169, 14: 196, 15: 225}

def square2(n):
    my_list = []

    while n >= 1:
        my_list.append((n, n*n))
        n -= 1

    my_list.reverse()

    my_list = dict(my_list)
    print(my_list)

square2(15)