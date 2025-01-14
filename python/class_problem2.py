# Write a Python class named Student with
# two attributes student_name, marks.
# Modify the attribute values of the said class
# and print the original and
# modified values of the said attributes.

'''
class Student:
    def __init__(self, student_name, marks):
        self.student_name = student_name
        self.marks = marks

s1 = Student('amirul', 95)

print(Student)
print(s1.student_name)
print(s1.marks)

print(getattr(Student, 'student_name'))
'''

class Student:
    student_name = 'amirul'
    marks = 95

s1 = Student()

print(getattr(Student, 'student_name'))
print(getattr(Student, 'marks'))

setattr(Student, 'student_name', 'imam')
setattr(Student, 'marks', 94)

print(getattr(Student, 'student_name'))
print(getattr(Student, 'marks'))

print('------------')

class Car:
    car1 = 'Land Rover'
    car2 = "Lamborghini"

print(getattr(Car, 'car1'))
print(getattr(Car, 'car2'))

setattr(Car, 'car2', 'Bugatti')

print(getattr(Car, 'car2'))