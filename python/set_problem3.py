# Write a Python program to check if a given
# value is present in a set or not.

my_set = {'a', 'b', 'c', 'd', 'e', 'f'}
user_input = 'f'

for i in my_set:
    #print(i)

    if i == user_input:
        print(user_input,'is present')

print('--------')

# Write a Python program to remove the
# intersection of a second set with a first set.

a = {1,2,3,4,5,6,7,8}
b = {3,4,10,12,6}

print(a-b)