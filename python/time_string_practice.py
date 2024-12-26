from datetime import datetime
a = "14, September, 2023"
b = datetime.strptime(a, '%d, %B, %Y')
print(b)
print(type(b))