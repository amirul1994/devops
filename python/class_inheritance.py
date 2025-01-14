class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return 'my name is {}'.format(self.name)

class Student(Person):

    def __init__(self, name, age, courses):
        self.courses = courses
        Person.__init__(self, name, age)

student_one = Student('amirul', '30', ['c', 'c++'])

print(student_one.introduce())