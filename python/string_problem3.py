#  Write a Python program to get a string from a given string where all occurrences of its first char have been changed to '$', except the first char itself.
# Sample String : 'restart'
# Expected Result : 'resta$t'

user_input = 'restart'
frequency = {}

for letter in user_input:
    first = user_input[0]
    keys = frequency.keys()

    if letter in keys:
        frequency[letter] += 1

    if letter not in keys:
        frequency[letter] = 1

    if frequency[letter] > 1:
        alt = user_input.replace(letter, '$')
        alt = first + alt[1:]
        print(alt)
        break


print(frequency)
#print(alt)