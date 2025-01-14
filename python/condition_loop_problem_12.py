# Write a Python program to find numbers between 100 and 400 (both included)
# where each digit of a number is an even number.
# The numbers obtained should be printed in a comma-separated
# sequence

for num in range(100, 401):
    if num%2 == 0:
        digit = str(num)
        if (int(digit[0])%2 == 0 and int(digit[1])%2 == 0 and
                int(digit[2]) %2 ==0):
            print(num)


print('----------')

for num in range(100, 401):
    all_even_digits = True
    for digit in str(num):
        if int(digit) % 2 != 0:
            all_even_digits = False
            break
    if all_even_digits:
        print(num)
