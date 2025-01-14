number_one = 2
number_two = 2

# id() will provide memory location for a variable
print(id(number_one))
print(id(number_two))
# 'is' will test if the variables are in the same memory location
# for the same location, it provides true otherwise false
my_list = []
my_list2 = []
print(id(my_list))
print(id(my_list2))
print(my_list is my_list2)
print(number_one is number_two)
print(number_one is not number_two)