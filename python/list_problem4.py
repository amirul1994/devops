# Write a Python program to remove duplicates from a list.

letter = ['a', 'a', 'n', 'c', 't', 'y', 'e', 'n', 'y', 't',
          'a', 't', 'a', 'c']

frequency = {}

letter2 = letter[:]
#print(letter2)

if len(letter) == 0:
    print('empty')
else:

 for char in letter:

    if char in frequency.keys():
        frequency[char] += 1
        letter2.remove(char)

    else:
        frequency[char] = 1

print(frequency)
print(letter2)

letter3 = list(letter2)
print(letter3)