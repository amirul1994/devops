def my_func(n):
    if n > 10:
        return
    print(n)
    my_func(n + 1)

    print(n)

my_func(1)


'''
The values of n are printed in reverse order because of how recursive function calls work in this specific code. Let me explain the sequence of events that leads to the values of n being printed in reverse order:

Initially, the function is called with n = 1. It prints 1 and then makes a recursive call to my_func(2).

The recursive call with n = 2 prints 2 and then makes another recursive call to my_func(3).

This process continues, with each recursive call incrementing n by 1 and printing the new value of n before making the next recursive call.

The recursion continues until n reaches 10. At this point, my_func(10) prints 10, and then a new recursive call to my_func(11) is made.

In the case of my_func(11), the conditional statement if n > 10: is true, so it immediately returns without printing anything. This is the base case that terminates the recursion.

As the recursion returns from my_func(11) to my_func(10), my_func(9), my_func(8), and so on, it continues to print the values of n after each recursive call returns.

Since the function is designed to print the value of n both before and after the recursive call, you see the values of n printed in increasing order up to 10, and then as the recursive calls return, you see the values of n printed again in reverse order from 10 down to 1. This is a characteristic of recursive functions that use a similar pattern to traverse a sequence or perform an operation on a range of values and then backtrack to return results.
'''