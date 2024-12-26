# Write a Python program to get the week number.
# Sample Date : 2015, 6, 16
# Expected Output : 25

import datetime

formatted_date = datetime.date(2015, 6, 16)

week_number = datetime.datetime.strftime(formatted_date, '%U')

print(week_number)

print('-------------')

# Write a Python program to find the date of the
# first Monday of a given week.
# Sample Year and week : 2015, 50
# Expected Output : Mon Dec 14 00:00:00 2015

import time

year = '2015'
week_number = '50'
week_day = 'monday'
week_day_number = '1'

formatted_date = datetime.datetime.strptime(
    '2015 50 1', '%Y %U %w')

print(formatted_date)

#print(datetime.date(formatted_date))

print(datetime.datetime.strftime(formatted_date, '%c'))
