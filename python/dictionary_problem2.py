# Write a Python script to add a key to a dictionary.
# Sample Dictionary : {0: 10, 1: 20}
# Expected Result : {0: 10, 1: 20, 2: 30}

dict1 = {0: 10, 1:20}
dict1[4] = 30
print(dict1)

print('***************')

#  Write a Python script to concatenate the following dictionaries to create a new one.
#
# Sample Dictionary :
# dic1={1:10, 2:20}
# dic2={3:30, 4:40}
# dic3={5:50,6:60}
# Expected Result : {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}

dic1 = {1:10, 2:20}
dic2 = {3:30, 4:40}
dic3 = {5:50, 6:60}

a1 = dic1.items()
print(a1)

a2 = dic2.items()
print(a2)

a3 = dic3.items()
print(a3)

a4 = tuple(a1) + tuple(a2) + tuple(a3)
print(a4)

dic4 = dict(a4)
print(dic4)

print('----------------')

# Write a Python script to check whether a given key
# already exists in a dictionary.

dictionary1 = {
    'name': 'amirul',
    'age': 30,
    'address': 'dhaka'
}

query = input('enter your query: ')

key = dictionary1.keys()
# print(key)

for i in key:
    # print(i)
    if query in i:
        print('found')
        break
    #if query not in i:
        # print('not found')
        # break

print('----------')

# Write a Python program to iterate over dictionaries
# using for loops.

dictionary2 = {
    'iman': 1,
    'malaika': 2,
    'kitab': 3,
    'rasul': 4,
    'takdir': 5,
    'akhirat': 6
}

for i in dictionary2.items():
    print(i)

for a, b in dictionary2.items():
    print(a, '----', b)