# Write a Python program to get the last day of a specified
# year and month and get the number of days in a given month and year.

import datetime
import calendar

def last_day(year, month):
    output = calendar.monthrange(year, month)
    #print(output)

    #weekday_number = output[0]
    total_days_in_month = output[1]

    #print(weekday_number)
    print(total_days_in_month)

    last_date = datetime.date(year, month, total_days_in_month)
    print(last_date)

    last_day_weekday = last_date.strftime('%A')
    print(last_day_weekday)

    print('the last day is {}, weekday is {}, the total day in'
          'the specified month is {}'
          ''.format(
        last_date, last_day_weekday, total_days_in_month))

    '''
    first_day = datetime.date(2024, 4, 1)
    print(first_day)
    print(first_day.strftime('%A'))
    '''

last_day(2024, 4)