# Write a Python program to generate all permutations of a list in Python.

my_list = [1, 2, 3, 4, 5]

# if all the elements is taken, the formula is permutation = n!
# n is the number of elements
a = 1

for i in my_list:
    a *= i

print(a)

# if only certain number of elements taken
# here 2 elements are taken
# the formula is P = n! / (n-r)!
# r is the number of elements taken

b = 1

for i in my_list:
    b *= i

permutation = b / (len(my_list) - 2)
print(permutation)