# Write a Python program to get the Fibonacci series between 0
# and 50.

c = [0,1]

while c[-1] + c[-2] <= 50:
    d = c[-1] + c[-2]
    c.append(d)

print(c)

i = 1

while i < len(c):
    print(c[i])
    i += 1