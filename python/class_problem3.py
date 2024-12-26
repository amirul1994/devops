# Write a Python class named Student
# with two attributes: student_id, student_name.
# Add a new attribute: student_class.
# Create a function to display all attributes
# and their values in the Student class.


class Student:
    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name

s1 = Student('asd', 'amirul')

setattr(s1, 'student_class', 'five')

print(s1.student_class)

print(getattr(s1, 'student_id'))