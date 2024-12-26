# meta class is the class of class
"""
class A:
    pass

obj = A()
"""

# obj is the instance of the class A

# a metaclass is a class that
# defines the behavior of other classes, known as its instances.

myStr = 'bohubrihi'
myNum = 10
myDict = {'name': 'amirul'}
myList = [1, 2, 3, 4]

class A:
    pass

obj = A()
print(type(obj))
print(type(A)) # type is a meta class

'''
print(type(myStr))
print(type(myNum))
print(type(myDict))
print(type(myList))
'''

# https://datacamp.org/community/tutorials/python-metaclasses