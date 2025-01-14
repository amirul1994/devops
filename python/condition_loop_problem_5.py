# Write a Python program that accepts a word from the user and
# reverses it.

a = input('type a word: ')

n = []

print(a)

for b in a:
    print(b)
    n.append(b)

print(n)

i = len(a) - 1

d = ''
while i >= 0:
    d += n[i]
    i = i - 1

print(d)
