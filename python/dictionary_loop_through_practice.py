cars = {
    "name": "nissan",
    "brand": "nissan",
    "mileage": 50000,
    "owners_list": ["a", "b"],
    "release": 2008
}

print(cars.keys())
print('**********')

print(cars.values())
print('***********')

print(cars.items())
print('**********')


for key in cars.keys():
    print(key)

print('**********')

for value in  cars.values():
    print(value)

print('**********')

for item in cars.items():
    print(item)

print('**********')

for key, value in cars.items():
    print(key, value)

print('**********')

for key in cars.keys():
    print(cars[key])