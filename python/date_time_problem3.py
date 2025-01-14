# Write a Python program to subtract five days from the current date.
# Sample Date :
# Current Date : 2015-06-22
# 5 days before Current Date : 2015-06-17

import datetime

difference1 = datetime.datetime.now() - datetime.timedelta(5)
print(difference1)

print('-----')

difference2 = datetime.date.today() - datetime.timedelta(5)
print(difference2)

print('--------')

print(datetime.datetime.now() - datetime.timedelta(3))

current_date = datetime.date.today()
day_difference = datetime.timedelta(2)

print('two days before: ', current_date-day_difference)
print('two days after: ', current_date+day_difference)

print('-------------')

print(datetime.datetime.now() + datetime.timedelta(hours=4))

print('-------')

a = datetime.datetime.now()
b = datetime.timedelta(hours = 8)
print(a+b)

print('------------')

print(datetime.datetime.now() + datetime.timedelta(hours = 7))

print('-------------')
print(datetime.datetime.now() + datetime.timedelta(hours = 5,
                                                   minutes = 15))
print('----------')
print(datetime.datetime.now() + datetime.timedelta(days = 2,
                                                   hours = 5,
                                                   minutes = 39))