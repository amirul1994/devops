# Write a Python program to count the number of characters (character frequency) in a string.

user = 'amirulmaula'

num_frequency = {}

for i in user:
    frequency = num_frequency.keys()
    print(frequency)

    if i in frequency:
        num_frequency[i] += 1

    else:
        num_frequency[i] = 1

print(num_frequency)