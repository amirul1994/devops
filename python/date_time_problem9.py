# Write a Python program to drop microseconds from datetime.
import datetime

def drop():
 current_time = datetime.datetime.now()
 print(current_time)

 changed_time = str(current_time).split('.')
 print(changed_time[0])

drop()

print('--------')

# Write a Python program to get days between two dates.
# Sample Dates : 2000,2,28, 2001,2,28
# Expected Output : 366 days, 0:00:00

def day_diff(d1, d2):
    changed_d1 = datetime.datetime.strptime(d1, '%Y,%m,%d')
    changed_d2 = datetime.datetime.strptime(d2, '%Y,%m,%d')
    print(changed_d2 - changed_d1)

day_diff('2000,6,29', '2001,2,28')
day_diff('2000,2,28', '2001,2,28')

print('---------------')

# Write a Python program to get the date of the last Tuesday.