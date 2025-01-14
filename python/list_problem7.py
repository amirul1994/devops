# Write a Python program to print a specified list
# after removing the 0th, 4th and 5th elements.
# Sample List : ['Red', 'Green', 'White', 'Black', 'Pink', 'Yellow']
# Expected Output : ['Green', 'White', 'Black']

user_input = ['Red', 'Green', 'White', 'Black', 'Pink', 'Yellow']

n = [0, 4, 5]
n = sorted(n)
n.reverse()
print(n)


j = 0

exp = user_input[:]

for a in user_input:
    if j < len(n):
        print(n[j])
        # use pop() to delete element by index number
        # use remove() to delete element by index value
        print(exp.pop(n[j]))
        j += 1

print(exp)

print('-----------')

user_input = ['Red', 'Green', 'White', 'Black', 'Pink', 'Yellow']

n = [0, 4, 5]

# Remove elements at the specified indices
for index in sorted(n, reverse=True):
    user_input.pop(index)

print(user_input)