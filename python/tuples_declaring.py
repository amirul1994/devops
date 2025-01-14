# tuples are immutable 
fruits = ("apple", "banana", "mango", 1, 2, 1.5, ["a", "b", "c"], 'mango')

print(fruits) 
print(type(fruits)) 

name = ("amirul",) 
print(type(name)) 

print(name[0])
print(name[-1]) 

'''
fruits[1] = 'orange' 
print(fruits)
''' 

fruits = list(fruits) 
fruits[1] = 'orange'  # type: ignore
print(fruits) 

fruits = tuple(fruits)
print(type(fruits)) 

cars = ("ferrari", "lamborghini", "mclaren", "bugatti", "tesla", "land rover", "bmw") 

i = 0 

while i < len(cars): 
    print(cars[i]) 
    i+=1 

n = 0
for n in  range(len(cars)): 

   print(cars[n])
   n+=1

a = 0 

while a <= 10: 
    print(a) 
    a+=2 

odd_numbers = (1, 3, 5, 7, 9)
even_numbers = (2, 4, 6, 8, 10)

numbers = odd_numbers + even_numbers
print(numbers)