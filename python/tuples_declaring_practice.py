cars = ("ferrari", "lamborghini", "mclaren", "bugatti", "tesla", "land rover", "bmw")
print(type(cars)) 

cars2 = "bugatti", "toyota", "honda", 1, 3.4, ["dsada", 'dsadas']
print(type(cars2)) 

cars3 = ('pazero',)
print(type(cars3))



cars3 = list(cars3) 

cars3.append("honda")  # type: ignore
print(cars3) 

cars3.pop(0)
print(cars3) 

cars3.insert(1, "chevrolette") # type: ignore
print(cars3) 

cars3.remove('honda')
print(cars3) 

cars3 = tuple(cars3)
print(type(cars3)) 


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


b = 0 

for b in range(b, 100, 2): 
    print(b)
    
print("----------")
b = 2 
step = b*3
for num in range(2, 100, step):
     print(num) 


odd_numbers = (1, 3, 5, 7, 9)
even_numbers = (2, 4, 6, 8, 10)

numbers = odd_numbers + even_numbers
print(numbers)