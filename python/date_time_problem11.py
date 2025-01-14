# Write a Python program to test the third Tuesday of a month.

import datetime

first_date = datetime.date(2023, 3, 1)
#print(first_date)

target_day_number = int(first_date.strftime('%w'))

#print(target_day_number)
#print(first_date.strftime('%A'))

given_day = 'Tuesday'

weekday = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
           'Thursday', 'Friday', 'Saturday']

given_day_number = weekday.index(given_day)

#print(given_day_number)

total_weekday = 7

difference = (target_day_number - given_day_number +
              total_weekday) % total_weekday

#print(difference)

target_date = first_date + datetime.timedelta(days = difference)
#print(target_date)

i = 1

for i in range(1,3):
    target_date += datetime.timedelta(days = 7)
    i += 1

#print('the third Tuesday is {} '.format(target_date))

formatted_date = target_date.strftime('%d %b %Y')

print('the third tuesday is {} '.format(formatted_date))