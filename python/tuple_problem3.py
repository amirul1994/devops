# Write a Python program to find repeated items in a tuple.
# check whether an element exists within a tuple.
# find the index of an item in a tuple.

tup = ('a', 'b', 'c', 'd', 'e', 'f', 'c', 'e', 'f')
frequency = {}
user_input = 'a'

for i in tup:
    key = frequency.keys()
    # print(key)
    # print(i)

    if i in frequency.keys():
        frequency[i] += 1
    else:
        frequency[i] = 1

    if frequency[i] > 1:
        print('{} appears more than once'.format(i))

print(frequency)

if user_input in frequency.keys():
    print('{} is found in {}'.format(user_input, tup))

tup2 = tup[1:4]
print(tup2)

tup3 = tup[2:7:2]
print(tup3)

tup4 = tup[2:7:3]
print(tup4)

print('----------')

index_num = 0

for i in tup:
    print(i,' is in index ', index_num)
    index_num += 1