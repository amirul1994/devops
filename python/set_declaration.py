fruits = {"apple", "mango", "orange", "apple", "orange"} 
print(fruits)
print(type(fruits))

fruits = set(["apple", "mango", "orange"])
print(fruits)
print(type(fruits)) 

# empty set 
'''
empty_set = {} 
print(type(empty_set))
''' 

empty_set = set()
print(type(empty_set)) 

cars = {"audi", "lamborghini", "mclaren"}
print(type(cars)) 

cars2 = set(("ferarri", 'landrover', "audi"))
print(type(cars2)) 

cars3 = set(["audi", 'chevrolette', 'toyota'])
print(type(cars3))

cars4 = set()
print(type(cars4)) 

# set is unordered unlike tuple, list
# in list & tuple, item can be accessed through index number
# in set, it is not possible 

fruits = {'apple', 'banana', 'orange', 'mango'} 
print('mango' in fruits)
print('kiwi' in fruits) 

cars = {"audi", "lamborghini", "mclaren"} 
print("audi" in cars)
print("land rover" in cars) 


user = {'amirul', 'maula'} 
print(user)

user.add("brinto")
print(user) 

user.add((1,2))
print(user) 

#user.add([1, 2])
#print(user) 

cars = {"audi", "lamborghini", "mclaren"} 
cars.add("ferarri")
print(cars) 

cars.add(('toyota',))
print(cars) 

user = {'amirul', 'maula', 'brinto'} 
user.remove('brinto') 
print(user) 

user = {'amirul', 'maula', 'brinto'}
user.discard('brinto')
print(user) 

cars = {"audi", "lamborghini", "mclaren"}  
cars.discard("audi")
print(cars) 

cars.remove("mclaren")
print(cars) 

user = {'amirul', 'maula', 'brinto'} 

for username in user: 
    print(username) 


cars = {"audi", "lamborghini", "mclaren"}   

for car in cars: 
    print(car) 


print("audi" in cars)

