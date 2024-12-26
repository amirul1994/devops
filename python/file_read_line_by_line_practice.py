file = open('D:/test.txt', 'r')

#print(file.read())

"""
print(file.readline())
print(file.readline())
print(file.readline())
print(file.readline()) 
"""

file2 = open('D:/test.txt', 'r')

'''
for line in file2:
    print(line)
'''

'''
while True:
   line = file.readline()
   if not line:
       break
   print(line)
   
'''

file2 = open('D:/test.txt', 'r')
print(file2.readlines())