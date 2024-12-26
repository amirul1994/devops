print('hi') 

flat = {'shewrapara', 'matikata', 'jatrabarti'} 

house = set(['mirpur', 'khilgaon']) 
print(type(house)) 

print("mirpur" in house) 

for number in house: 
    print(number) 

house.add('boshundhara')
print(house) 

house.add('niketon')
print(house)

house.remove('boshundhara')
print(house)

house.discard('boshundhara')
print(house) 

cars = ('ferarri',)
print(type(cars)) 

cars2 = "audi", 'bugatti'

cars3 = cars+cars2

print(cars3)
print(cars) 

for car in cars3: 
    print(car)

print(cars3[1]) 

food = ["meat", "chicken", "fish"]
food.append("vegetable")
print(food) 

food.insert(1, 'curry')
print(food) 

food.pop() 
print(food) 

food.pop(1)
print(food)

food.remove('fish')
print(food) 

name = 'amirul maula'
name.split()
print(name)

name2 = name.split()
print(name2) 

name3 = name.split( )
print(name3) 

name = 'amirul maula,brinto' 
name4 = name.split(",")
print(name4) 

a = "amirul"
print(a.split())

print(a.split(" ")) 
print(a.split("'' ''"))
print(a.split('"')) 

a = "amirul" 
print(a[1:2]) 

txt = "Hello World" [::-1]
print(txt)