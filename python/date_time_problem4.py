# Write a Python program to convert a Unix timestamp
# string to a readable date.
# Sample Unix timestamp string : 1284105682
# Expected Output : 2010-09-10 13:31:22

import datetime
import time

print(time.localtime(1284105682))

print('---------')

print(datetime.datetime.fromtimestamp(1284105682))

print(datetime.datetime.fromtimestamp(123456))

print('------------')

# Write a Python program to print yesterday, today, tomorrow.

today = datetime.date.today()
print(today)

yesterday = today - datetime.timedelta(days = 1)
print(yesterday)

tomorrow = today + datetime.timedelta(days = 1)
print(tomorrow)

print('------------')

# Write a Python program to convert the
# date to datetime (midnight of the date) in Python.
# Sample Output : 2015-06-22 00:00:00


today = datetime.datetime.now()
print(today)
print(today.replace(hour = 0, minute = 0, second = 0))

print('---------')

current_date = datetime.date.today()

midnight = datetime.datetime(year = current_date.year,
                                   month = current_date.month,
                                   day = current_date.day)
print(midnight)

print('---------')

user_input = '03-06-2009'

formatted_date = datetime.datetime.strptime(user_input,
                                            '%d-%m-%Y')
print(formatted_date)

user_input2 = '03 Jun 2009'
print(datetime.datetime.strptime(user_input2, '%d %b %Y'))


print('-----------')

# Write a Python program to print the
# next 5 days starting today.

today = datetime.date.today()

for i in range(1, 6):
    print(today + datetime.timedelta(i))

print('--------')

print(datetime.datetime.now())
print(datetime.datetime.now() + datetime.timedelta(seconds = 5))