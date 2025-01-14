username = "amirul maula"
print(username.upper())
print(username.lower()) 

welcome_text = 'welcome to python'
modified_text = welcome_text.replace('python', 'javascript')
print(modified_text) 

text = 'this is good!!!'
print(text.replace('!', '#', 1)) 

first_name = "amirul"
last_name = "maula" 

full_name = "{} {}".format(first_name, last_name)
print(full_name) 

a = 100 
b = 123 

print("{}{}".format(a, b)) 
print("{} {}".format(a, b)) 

c = 'jalal'
d = 'ahmed' 
e = "uddin"

full_name2 = "{f} {g} and h is {h}" .format(f = c, g = d, h = e)
print(full_name2) 

i = 'I'
j = 'am' 
k = 'male' 

print("{l} {m} {n}".format(l = i, m = j, n = k))