# Write a Python program to count the occurrences of each word in a given sentence.

user_input = 'my name is amirul my'

my_list = user_input.split(' ')
print(my_list)

frequency = {}

for word in my_list:
    key = frequency.keys()

    if word in key:
        frequency[word] += 1
    else:
        frequency[word] = 1

print(frequency)