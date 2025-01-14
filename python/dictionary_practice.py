car = {
    "brand": "audi",
    "price": "400k",
    "owner": ['a', 'b'],
    'origin': {"UK", "USA"},
    "asdad": ("sadad", "asdasds"),
    "lmn": {
        "asdasd": "trt",
        "qwerty": "rfsdsfs"
    }
}

print(car)
print(type(car))
print(car['origin'])
print(car["owner"])
print(car["lmn"]["asdasd"])
print(car["owner"][0])

#print(car["rt"])
print(car.get("rt"))
print(car.get("brand"))

car["brand"] = "nissan"
car['price'] = "300k"

print(car["brand"])
print(car["price"])

car.update(
    {
        "brand": "ferarri",
        "price": "500k"
    }
)

print(car)

car["year"] = "2015"
print(car)

car.update(
    {
        "manufacturer": "ferarri"
    }
)
print(car)

del car["lmn"]
print(car)

car.pop("asdad")
print(car)

car2 = car.copy()
print(car2)