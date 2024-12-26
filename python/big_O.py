# Big O is the language and metric we use to describe
# the efficiency of algorithms

# Algorithm run time notations
# - Best Case
# - Average Case
# - Worst Case

# Time Complexity:
# Time complexity in computer science is a way of expressing
# how the running time of an algorithm grows
# relative to the size of its input.

# Space Complexity:
# Space complexity in computer science is about
# how much memory an algorithm needs based
# on the size of the data it handles.
# here memory means mainly ram and storage

# Big O, Big Omega & Big Theta
# For Interview only Big O is necessary

# Big O: It is a complexity that is going to be
# less or equal to the worst case

# Algorithm run time complexities

# Complexity   Name        Sample
# O(1)       Constant    Accessing a specific element in array
# O(N)       Linear      Loop through array elements
# O(logN)    Logarithmic  Find an element in sorted array
# O(N^2)     Quadratic    Looking every index in the array twice
# O(2^N)     Exponential  Double recursion in Fibonacci

# Drop constant and non-dominant factors:
# This makes our life easier to compare our algorithm
# without depending on the characteristics of computer
# and computational complexity of different operations

# O(2N) - drop 2 - O(N)
# O(N+logN) - drop log(N) - O(N)

# How to measure the codes using Big O?

# Rule 1 - Any assignment statements and if statements that are
# executed once regardless of the size of the problem
# complexity - O(1)

# Rule 2 - A simple 'for' loop from 0 to n ( with no internal
# loops); complexity - O(n)

# Rule 3 - A nested loop of the same type takes quadratic time
# complexity; complexity - O(n^2)

# Rule 4 - A loop, in which the controlling parameter is
# divided by two at each step; complexity - O(log n)

# Rule 5 - When dealing with multiple statements, just add
# them up 