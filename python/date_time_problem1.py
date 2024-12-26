# Write a Python script to display the various Date Time formats -
# a) Current date and time
# b) Current year
# c) Month of year
# d) Week number of the year
# e) Weekday of the week
# f) Day of year
# g) Day of the month
# h) Day of week


import time
import datetime

# a) Current date and time
print(time.ctime())
print(datetime.datetime.now())

print('------------')

# b) Current year
print(datetime.datetime.now().year)

print('------------')

# c) Month of year
print(datetime.datetime.now().month)

print('-----------')

# d) week number of the year
print(datetime.datetime.now().strftime('%U'))
print('----------')

# e) weekday of the week
print(datetime.datetime.now().strftime('%w'))
print('--------------')

# h) day of the week
print(datetime.datetime.now().strftime('%A'))
print('---------------')

# f) day of year
print(datetime.datetime.now().strftime('%j'))
print('-----------')

# g) day of the month
print(datetime.datetime.now().strftime('%d'))
