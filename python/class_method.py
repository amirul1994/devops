# instance attribute represents the state of the object for
# the particular class

# class attribute will represent the state of the class

class Student:
    # 'school_name' will define common value for the objects
    # in the 'Student' class
    # in other words it will represent a state of the class
    school_name = 'test school'
    def __init__(self,name, course):
        self.name = name
        self.course = course

    # for class method instead of 'self',
    # 'cls' is used
    # 'cls' indicates the particular class
    # a special syntax is used for class method
    # is known as decorator

    @classmethod
    def get_school_name(cls):
        return cls.school_name

student_one = Student("s1", "c1")
student_two = Student("s2", 'c2')

# in class method to call the method,
# class name has to be used
print(Student.get_school_name())