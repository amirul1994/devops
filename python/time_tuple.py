import datetime

current_date_time = datetime.datetime.now()
print(current_date_time.timetuple())

struct_time_obj = current_date_time.timetuple()
print(struct_time_obj[0])

import time

a = datetime.date.fromtimestamp(1234567832)
print(a)

b = a.timetuple()
print(b)
print(b[3])
print(b[6])