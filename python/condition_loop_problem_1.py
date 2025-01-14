# Write a Python program to find those numbers which are divisible by 7 and multiples of 5, between 1500 and 2700 (both included).

for a in range(1500, 2700):
    if a%7 == 0 and a%5 == 0:
        print('{} is divisible by 7 and '
                    'multiplies of 5'.format(a))
