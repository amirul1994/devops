""" car_models = ["bmw", "toyota", "audi", 1, 2, 1.45, ["1", "2", "3"]] 

countries = ["bangladesh", "india", "germany", "norway", "china"] 

print(countries)
print(countries[2]) 

print(car_models[6][1]) 
print(car_models[-1]) 

car_models[2] = 'bugatti'
print(car_models) 

del countries[1]
print(countries)

del countries[3]
print(countries) 

del countries[-1]
print(countries) 


fruits = ['banana', 'mango', 'apple', 'orange']
fruits.pop() 
removed_item = fruits.pop()
print(fruits)
print(removed_item) 

another_removed_item = fruits.pop(0)
print(fruits) 

vowels = ['a', 'e', 'i', 'o', 'i', 'u'] 
vowels.remove('i') 
print(vowels) 

house = [1, 2, 3, 4, 5, 6, 7, 8, 9, [10, 11, 12]] 

del house[2] 
print(house) 

del house[-3]
print(house) 

house.pop()
print(house) 

house.pop(4)
print(house)

# remove() will delete the item mentioned inside ()
house.remove(2)
print(house) 

house.remove(7)
print(house) """

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] 

# numbers[start:end:step]
# default 
# start = 0 
# end = -1 
# step = 1
print(numbers[2:6]) 
print(numbers[:6]) 
print(numbers[2:6:2])
print(numbers[-1:-11:-1])
print(numbers) 

number = [1, 2, 3, 4, 5, 6, 7]

print(number[1:5:3])

number.sort()
print(number) 

number.sort(reverse=True) 
print(number) 

number2 = ['man', 'child', 'woman']
number2.sort()
print(number2) 

number2.sort(reverse=True)
print(number2) 

number3 = [45, 32, 78, -4, 100]
print(sorted(number3)) 
print(number3) 
print(sorted(number3, reverse=True)) 



number4 = [13, 25, 78, 6, 435]
print(sorted(number4)) 
print(sorted(number4, reverse=True))
number4.sort() 
print(number4)
number4.sort(reverse=True)
print(number4)

number5 = number4.copy()
print(number5)

number6 = number5[:]
print(number6)

number7 = [1, 2, 3, 4, 5]
number8 = [6, 7, 8, 9, 10] 

number9 = number7 + number8
print(number9)  

veg = ['papaya', 'raddish']
veg2 = ['potato', 'tomato']

print(veg+veg2)

veg.extend(veg2)
print(veg)

number7.extend(number8)
print(number7)

number7.append(190)
print(number7) 

number7.append(67)
print(number7) 

number7.insert(0, -5)
print(number7)

number7.insert(6, 64)
print(number7)

print(number7.count(23))
print(number7.count(10)) 

"You can find the list methods here:"
"https://docs.python.org/3/tutorial/datastructures.html"