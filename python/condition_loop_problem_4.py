'''
Write a Python program to construct the following pattern, using a nested for loop.

*
* *
* * *
* * * *
* * * * *
* * * *
* * *
* *
*
'''

a = ['*', '**', '***', '****', '*****']

def star():
    for b in a:
        print(b)

    i = len(a) - 2

    while i >= 0:
        print(a[i])
        i = i - 1

star()