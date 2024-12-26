#  Write a Python program to guess a number between 1 and 9.

import random

a = random.randint(1, 10)

def guess():
    b = int(input('guess a number: '))

    while b != a:
        b = int(input('guess a number: '))

    if b == a:
        print('well guessed!')

guess()