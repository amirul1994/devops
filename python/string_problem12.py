# Write a Python function to create an HTML string with
# tags around the word(s).
# Sample function and result :
# add_tags('i', 'Python') -> '<i>Python</i>'
# add_tags('b', 'Python Tutorial') -> '<b>Python Tutorial </b>'

def add_tags(i, Python):
    str1 = ""
    print(Python+str1)
    print('<' + i + '>' + Python + '<' + i + '>' )


add_tags('i', 'Python')
add_tags('b', 'Python')