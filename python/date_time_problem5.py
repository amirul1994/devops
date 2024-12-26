import datetime

# Write a Python program to convert Year/Month/Day
# to Day of Year in Python.

user_input = '1998/05/23'
formatted_date = datetime.datetime.strptime(user_input,
                                            '%Y/%m/%d')
print(formatted_date)
print(formatted_date.strftime('%j'))

print('---------')

# Write a Python program to get the
# current time in milliseconds in Python.

import time

# time.time() will return value in seconds spent till 01 Jan 1970
print(time.time() * 1000)