# Write a Python program to count the number of strings
# from a given list of strings. The string length is 2
# or more and the first and
# last characters are the same.

user_input = ['abc', 'xyz', 'aba', '1221']
rpt = []

print(len(user_input))

for i in user_input:
    if len(i) >= 2 and i[0] == i[-1]:
        print(i)
        rpt.append(i)

print(rpt)
print(len(rpt))





