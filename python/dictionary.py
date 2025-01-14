student = {"name": "amirul maula", "age": 8, "courses" :[
    "python", "java", "c++"]}

empty_dictionary = {}
print(empty_dictionary)
print(type(empty_dictionary))

empty_dictionary = dict()
print(type(empty_dictionary))

student2 = {"name": "renesa", "age":24, "course":["php",
                                                  "python", "java"]}
print(student2)
print(type(student2))

empty = {}
print(empty)

empty = dict()
print(empty)

employee = {
    "name": "amirul maula",
    "skills": ["python", "django", "go"],
    "years_of_experience": 4
}

print(employee["name"])
print(employee["skills"])
# print(employee["salary"])

print(employee.get('name'))
print(employee.get("salary"))

# provide a value for non-existing key
print(employee.get("salary", "not found!"))

employee = {
    "name": "amirul maula",
    "skills": ["python", "django", "go"],
    "years_of_experience": 4
}

employee["name"] = "test user"
print(employee["name"])

employee["years_of_experience"] = 8
print(employee["years_of_experience"])

employee.update(
    {
        "name": "test user 2",
        "years_of_experience": 6
    }
)

print(employee)

employee = {
    "name": "amirul maula",
    "skills": ["python", "django", "go"],
    "years_of_experience": 4
}

employee["company name"] = "cefalo bangladesh ltd"
print(employee)

employee.update(
    {
        "address": "dhanmondi",
        "type": "permannet"
    }
)

print(employee)

del employee["type"]
print(employee)

employee.pop("address")
print(employee)

student2 = student.copy()
print(student2)