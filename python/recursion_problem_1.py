# Write a Python program to calculate the sum of a list of numbers.

'''
my_list = [1, 2, 3, 4, 5]

def sum(b):
    add = 0

    for a in b:
        add += a

    print(add)

sum(my_list)
'''


def sum(a):
    if len(a) == 1:
        return a[0]

    if len(a) > 1:
        return a[0] + sum(a[1:])

print(sum([1,2,3,4,5]))
print(sum([5]))