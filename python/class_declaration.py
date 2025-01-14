"""
class Person:
    name = 'amirul maula'

obj1 = Person()
obj2 = Person()

print(obj1)
print(type(obj1))


class Car:
    name = 'ferarri'

a = Car()
print(a)
print(type(a))
"""

class Person:
    # __init__() method is called when any object is created
    # in a class, this method works as same as constructor
    # 'self' is used as to store the object
    # here it will be person one or person two
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def introduce(self):
        return 'my name is {}'.format(self.name)

person_one = Person('amirul', 30, 'male')
person_two = Person('user two', 24, 'female')

print(person_one.name)
print(person_one.age)
print(person_one.gender)

print(person_one.introduce())
print(person_two.introduce())