# Write a Python program to sum and multiply all the items in a
# list.

user_input = [1, 2, 3, 5, 6]

sum = 0
multiplication = 1

for i in user_input:
    sum += i
    multiplication *= i

min_num = min(user_input)
max_num = max(user_input)

print(min_num)
print(max_num)
print(sum)
print(multiplication)