# Write a Python program to create
# two empty classes, Student and Marks.
# Now create some instances and check whether
# they are instances of the said classes or not. Also, check whether
# the said classes are subclasses of the built-in object class
# or not.

class student:
    pass

class marks:
    pass


c1 = student()
c2 = marks()

print(isinstance(c1, student))
print(isinstance(c2, student))
print(isinstance(c1, marks))
print(isinstance(c2, marks))

print('-------------')

print(issubclass(student, marks))
print(issubclass(marks, student))