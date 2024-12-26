# Write a Python program to sort a tuple by its float element.
# Sample data: [('item1', '12.20'), ('item2', '15.10'), ('item3', '24.5')]
# Expected Output: [('item3', '24.5'), ('item2', '15.10'), ('item1', '12.20')]

def max(i):
 return (i[-1])

def sort_my_list(my_list):
    return sorted(my_list, key = max, reverse = True)


print(sort_my_list([('item1', '12.20'), ('item2', '15.10'),
              ('item3', '24.5'), ('item4', '13.10')]))

print('--------------')

def sort_list(my_list):
    sorted_list = sorted(my_list, key = lambda n: n[-1],
                         reverse = True)
    print(sorted_list)


sort_list([('item1', '12.20'), ('item2', '15.10'),
              ('item3', '24.5'), ('item4', '13.10')])