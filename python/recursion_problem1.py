# Write a Python program to calculate the
# sum of a list of numbers.

my_list = [1, 2, 3, 4, 5]
def sum(my_list):

    if not my_list:
        return 0
    else:
        return my_list[0] + sum(my_list[1:])


print(sum(my_list))
print('---------')


# Write a Python program to get
# the factorial of a non-negative integer.

my_list2 = [1, 2, 3, 4, 5]

def multi(my_list2):
    if not my_list2:
        return 1
    else:
        return my_list2[0] * multi(my_list2[1:])

print(multi(my_list2))