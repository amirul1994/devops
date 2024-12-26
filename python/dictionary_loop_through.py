employee = {
    "name": "sifat hasan",
    "skills": ['python', 'django', 'go'],
    'years_of_experience': 4,
    'company': 'cefalo bangladesh ltd',
    "address": 'dhanmondi',
    "type": 'permanent'
}

# keys() return the keys of a dictionary as a list
print(employee.keys())
print("------------")
# values() return the all the values of a dictionary
print(employee.values())
print("------------")
# items() will return both key and value in tuples inside
# an array

print(employee.items())
print("------------")

for current_key in employee.keys():
    print(current_key)

print("------------")

for current_key in employee.keys():
    print(current_key, employee[current_key])

print("------------")

for key, value in employee.items():
    print(key, value)