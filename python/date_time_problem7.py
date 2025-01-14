# Write a Python program to select specified day in a specified
# year.
import datetime
def find_day(year,given_day):
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday']

    target_weekday = weekdays.index(given_day)
    print(target_weekday)
    #print(year)
    dd = year + ' 01 01'
    #print(dd)
    dd2 = datetime.datetime.strptime(dd,
                                     '%Y %m %d')
    #print(type(dd2.strftime('%w')))
    weekday_number = int(dd2.strftime('%w'))
    print(weekday_number)

    total_weekday = 7

    difference = (target_weekday - weekday_number + total_weekday) % total_weekday
    #print(difference)

    designated_day = dd2 + datetime.timedelta(difference)
    print(designated_day)

    while designated_day:
        designated_day += datetime.timedelta(7)
        if designated_day.year == int(year) + 1:
            break
        print(designated_day)

find_day('2020', 'Friday')
print('-----------')
find_day('2020', 'Sunday')
print('------------')
find_day('2020', 'Wednesday')
print('--------')

def find_day2(year, given_day):
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday']
    target_day = weekdays.index(given_day)
    print(target_day)

    full_date = str(year) + ' 01 01'

    converted_date = datetime.datetime.strptime(full_date,
                                                '%Y %m %d')

    converted_date_number = int(converted_date.strftime('%w'))
    print(converted_date_number)

    total_weekdays = 7

    difference = (target_day - converted_date_number + total_weekdays) % total_weekdays
    print(difference)

    designated_day = converted_date + datetime.timedelta(
        difference)
    print(designated_day)

    while designated_day:
        designated_day += datetime.timedelta(7)
        if designated_day.year != int(year):
            break
        print(designated_day)


find_day2(2020, 'Tuesday')
