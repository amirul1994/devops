# Write a Python program to print a string five times,
# with a delay of three seconds.

import time

user_input = 'write'

i = 0

for i in range(5):
    print(user_input)
    time.sleep(3)
    i += 1