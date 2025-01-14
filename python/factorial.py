def factorial(n):
    if n == 1:
        return 1

    print(n)

    m = factorial(n-1)

    print(n)

    return n * m

print(factorial(5))

'''
When you call factorial(5), it will calculate the factorial of 5 as follows:

factorial(5) calls factorial(4) and stores the result in m, where m is now equal to 24 (4!).

factorial(4) calls factorial(3) and stores the result in m, where m is now equal to 6 (3!).

factorial(3) calls factorial(2) and stores the result in m, where m is now equal to 2 (2!).

factorial(2) calls factorial(1) and stores the result in m, where m is now equal to 1 (1!).

factorial(1) returns 1.

Now, the recursive calls start to unwind:

factorial(2) returns 2 * 1, which is 2.

factorial(3) returns 3 * 2, which is 6.

factorial(4) returns 4 * 6, which is 24.

Finally, factorial(5) returns 5 * 24, which is 120.
'''