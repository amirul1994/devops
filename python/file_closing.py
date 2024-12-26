'''
file = open('D:/test.txt', 'r')
print(file.read())
file.close()
'''

# the importance of file closing is
# unless the file is closed it will
# occupy an amount of memory

# 'with' can be used to open a file
# 'file' is the variable
# the benefit of 'with' is, there is no need
# for explicitly mentioning of closing the file
"""
with open('D:/test.txt', 'r') as file:
    print(file.read())
"""

#print('------------')

#file2 = open('D:/test.txt', 'r')
#print(file2.read())
#file2.close()


#print('***********')

"""
with open('D:/test.txt', 'r') as file2:
    print(file2.read())
"""

'''
file3 = open('D:/test2.txt', 'r')
#print(file3.read())
print(file3.readline())
print(file3.readlines())
#print(file3.close())
file3.close()
'''
# 'with' is the context manager

with open('D:/test2.txt', 'r') as file3:
    print(file3.readlines())
