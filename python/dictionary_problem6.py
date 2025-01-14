# Write a Python program to sort a given dictionary by key.

def value(tup):
    return tup[0]

def sort_by_key(my_dict):
    res = sorted(my_dict.items(), key= value)
    print(res)

sort_by_key({'n': 1, 'j':2, 'b': 3, 'q': 4})

print('-------')

def sort_by_key2(my_dict):
    res = sorted(my_dict.items(), key= lambda tup:tup[0])
    print(res)

sort_by_key2({'n': 1, 'j':2, 'b': 3, 'q': 4})