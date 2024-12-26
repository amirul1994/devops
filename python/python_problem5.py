# Write a Python program to find the first appearance of the substrings 'not'
# and 'poor' in a given string. If 'not' follows 'poor',
# replace the whole 'not'...'poor' substring with 'good'. Return the resulting string.
# Sample String : 'The lyrics is not that poor!'
# 'The lyrics is poor!'
# Expected Result : 'The lyrics is good!'
# 'The lyrics is poor!'

user_input = 'The lyrics is not that poor!'

my_list = user_input.split(' ')
print(my_list)

n = 0

for i in my_list:
    if i == 'not':
        print(" 'not' substring found, the index number is {"
              "} and the position is {}".format(n, n+1))
    elif i == 'poor!':
        print(" 'poor!' substring found, the index number is {"
              "} and the position is {}"
              .format(n, n+1))

    n += 1

print(" The length of the list is ", len(my_list))

my_list2 = my_list[0:3]

new = 'good!'

my_list2.append(new)
print(my_list2)

result = " ".join(my_list2)
print(result)