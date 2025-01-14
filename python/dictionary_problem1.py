# Write a Python script to sort (ascending and descending)
# a dictionary by value.

my_dictionary = {'age1': 30,
                 'age2': 25,
                 'age3': 61,
                 'age4': 70,
                 }

def value(values):
    return values[-1]

def sort_dictionary(my_dictionary):
    res = sorted(my_dictionary.items(), key=value)
    print(res)

    res = dict(res)
    print(res)

sort_dictionary(my_dictionary)

print('------------')
def reverse_sort_dictionary(my_dictionary):
    res2 = sorted(my_dictionary.items(), key = value,
                  reverse=True)
    print(res2)
    res2 = dict(res2)
    print(res2)

reverse_sort_dictionary(my_dictionary)