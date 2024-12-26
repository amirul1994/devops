# Write a Python program to get the date of the last Tuesday of
# a specified year

import datetime
date_list = []
def find_day(year, given_day):
    weekday = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
               'Thursday', 'Friday', 'Saturday']
    target_day = weekday.index(given_day)
    #print(target_day)

    first_date = datetime.date(year, 1, 1)

    first_date_number = int(first_date.strftime('%w'))

    #print(first_date_number)

    total_weekday = 7

    difference = (target_day - first_date_number +
                  total_weekday) % total_weekday

    #print(difference)

    designated_date = first_date + datetime.timedelta(difference)

    #print(designated_date)



    #date_list.append(designated_date)

    while designated_date.year == year:
        print(designated_date)
        date_list.append(designated_date)
        designated_date += datetime.timedelta(7)

        if designated_date.year != year:
            break

    #print(date_list[-1])


find_day(2021, "Tuesday")
print('--------')
print(date_list[-1])

print('**************************')

# Write a Python program to get the date of the last Monday

current_day2 = datetime.datetime.now()


print(current_day2)
print(current_day2.strftime('%A'))

weekday2 = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
               'Thursday', 'Friday', 'Saturday']

target_day = weekday2.index('Monday')
print(target_day)

current_day_number2 = int(current_day2.strftime('%w'))

total_weekday = 7

difference2 = ((target_day - current_day_number2 + total_weekday)
              % total_weekday)
print(difference2)

designated_day2 = current_day2 + datetime.timedelta(day = 7)
print(designated_day2)