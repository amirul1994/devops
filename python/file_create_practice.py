"""
a = open('test_file_3.txt', 'w')
a.write("this is line 1")
"""

cars = [
    {
        'name': 'ferarri',
        'brand': "ferarri"
    },

    {
        'name': 'bugatti',
        'brand': 'bugatti'
    }
]

with open('test_file_3.txt', 'w') as b:
    b.write(cars[1]['name'])







