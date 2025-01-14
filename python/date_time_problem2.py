# Write a Python program to convert a string to datetime.
# Sample String : Jan 1 2014 2:43PM
# Expected Output : 2014-07-01 14:43:00

import datetime

#print(datetime.datetime.strftime('Jan 1 2014 2:43PM',
                                 #'%b %d %Y %I:%M%p'))

print(datetime.datetime.strptime('Jan 1 2014 2:43PM',
                                 '%b %d %Y %I:%M%p'))


print(datetime.datetime.strptime('Feb 26 2015 10:12am',
                                 '%b %d %Y %I:%M%p'))

print(datetime.datetime.strptime('Mar 16 2011 1:13pm',
                                 '%b %d %Y %I:%M%p'))

print(datetime.datetime.strptime('2 Jun 2021 3:30AM',
                                 '%d %b %Y %I:%M%p'))

a = '2020 12 Jul 11:20PM'
print(datetime.datetime.strptime(a,
                                 '%Y %d %b %I:%M%p'))