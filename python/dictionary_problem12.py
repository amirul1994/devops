# Write a Python program to combine values in a list of dictionaries.
# Sample data: [{'item': 'item1', 'amount': 400},
# {'item': 'item2', 'amount': 300}, {'item': 'item1', 'amount': 750}]
# Expected Output: Counter({'item1': 1150, 'item2': 300})

my_dict = [{'item': 'item1', 'amount': 400},
           {'item': 'item2', 'amount': 300},
           {'item': 'item1', 'amount': 750}]


total = {}

for i in my_dict:
    item = i['item']
    amount = i['amount']

    if item in total:
        total[item] += amount
    else:
        total[item] = amount

print(total)