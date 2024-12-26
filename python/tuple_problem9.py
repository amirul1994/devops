# Write a Python program to check if a specified element appears
# in a tuple of tuples.
# Original tuple:
# (('Red', 'White', 'Blue'), ('Green', 'Pink', 'Purple'), ('Orange', 'Yellow', 'Lime'))
# Check if White present in said tuple of tuples!
# True
# Check if White present in said tuple of tuples!
# True
# Check if Olive present in said tuple of tuples!
# False


def find(tup, colour):
    for i in tup:
        # print(i)
       for n in i:
           #print(n)
           if colour in n:
                print('True')


find((('Red', 'White', 'Blue'), ('Green', 'Pink', 'Purple'),
      ('Orange', 'Yellow', 'Lime')), 'White')
