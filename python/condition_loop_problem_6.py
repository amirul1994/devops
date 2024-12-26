# Write a Python program to count the number of even and odd
# numbers in a series of numbers

numbers = (1, 2, 3, 4, 5)
# print(type(numbers))

i = 0
n = 0

for a in numbers:

    if a % 2 == 0 :
        i += 1
    else:
        n += 1


print('the number of even number is {}'.format(i))
print('the number of odd number is {}'.format(n))

