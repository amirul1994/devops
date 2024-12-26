# Write a Python program that accepts a string and calculates the number of digits and letters.
# Sample Data : Python 3.2
# Expected Output :
# Letters 6
# Digits 2

num_list = '0123456789'
user_data = 'amirul 8.3'

user_data2 = user_data.split()
user_data3 = ''.join(user_data2)

letter_count = 0
digit_count = 0

for char in user_data3:
    if char in num_list:
        digit_count += 1
    elif char.isalpha():
        letter_count += 1

print("Letters", letter_count)
print("Digits", digit_count)


print('--------------')

user_data = 'amirul 8.3'

# Initialize counters for letters and digits
letter_count = 0
digit_count = 0

# Iterate through each character in the string
for char in user_data:
    if char.isalpha():
        letter_count += 1
    elif char.isdigit():
        digit_count += 1

# Output the results
print("Letters", letter_count)
print("Digits", digit_count)
