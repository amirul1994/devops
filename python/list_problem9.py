# Write a Python program to generate and print a list
# of the first and last 5 elements where the values
# are square numbers between 1 and 30 (both included).

square_number_list = []

for i in range(1, 60):

    if i**2 <= 60:
        print(i**2)
        square_number_list.append(i**2)

print('the square numbers between 1 to 60 : {} '
      ''.format(square_number_list))

index_number = 0

first_five = []

while index_number < 5:
    a = square_number_list[index_number]
    first_five.append(a)
    index_number += 1

print('the first five elements are {}'.format(first_five))

index_number2 = -1

last_five = []

while index_number2 >= -5:
    b = square_number_list[index_number2]
    last_five.append(b)
    index_number2 = index_number2 - 1

print('the last five elements are {}'.format(last_five))

# Generate a list of square numbers between 1 and 30
square_numbers = [x**2 for x in range(1, 6)] + [x**2 for x in range(26, 31)]

# Print the first 5 and last 5 elements
first_5 = square_numbers[:5]
last_5 = square_numbers[-5:]

print("First 5 square numbers between 1 and 30:", first_5)
print("Last 5 square numbers between 1 and 30:", last_5)
