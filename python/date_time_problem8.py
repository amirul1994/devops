# Write a Python program to add year(s) to a given date
# and display the updated date.
#
# Sample Data : (addYears is the user defined function name)
# print(addYears(datetime.date(2015,1,1), -1))
# print(addYears(datetime.date(2015,1,1), 0))
# print(addYears(datetime.date(2015,1,1), 2))
# print(addYears(datetime.date(2000,2,29),1))
#
# Expected Output :
# 2014-01-01
# 2015-01-01
# 2017-01-01
# 2001-03-01


import datetime

def add_years(given_date, add_year):
    year = int(given_date['year'])
    #print(year)

    changed_year = year + add_year

    month = int(given_date['month'])

    day = int(given_date['day'])

    print(datetime.date(changed_year, month, day))

user_input = {'year': '2016', 'month': '3', 'day': '20'}
user_input2 = {'year': '2007', 'month': '3', 'day': '20'}

add_years(user_input, 2)
add_years(user_input2, -2)