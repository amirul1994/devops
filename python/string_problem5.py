# Write a Python program to add 'ing' at the end
# of a given string (length should be at least 3).
# If the given string already ends with 'ing', add 'ly' instead.
# If the string length of the given string is less than 3, leave it unchanged.
# Sample String : 'abc'
# Expected Result : 'abcing'
# Sample String : 'string'
# Expected Result : 'stringly'

def concat(user_input):

 if len(user_input) < 3:
    print(user_input)

 elif len(user_input) >= 3:
   i = -3
   if (user_input[i] == 'i' and user_input[i+1] == 'n' and
            user_input[i+2] == 'g'):
        print(user_input + 'ly')

   else:
       print(user_input + 'ing')

concat('abc')
concat('abcing')
concat('ab')
