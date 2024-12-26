# Write a Python program that finds all pairs of elements in a
# list whose sum is equal to a given value.

def find_pairs(my_list, value):
    pair = []
    for i in my_list:
        complement = value - i

        if complement in my_list:
            pair.append({i, complement})

    print(pair)



value = 36
find_pairs([10, 12, 15, 8, 26, 17, 19], value)