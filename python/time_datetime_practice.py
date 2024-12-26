import time

print(time.time())
print(time.ctime())
print(time.sleep(1))
print(time.localtime())

import datetime

print(datetime.datetime.now())
print(datetime.datetime.utcnow())

print(datetime.date.today())
print(datetime.date.fromtimestamp(13467891))
print(datetime.date.fromtimestamp(13467891).year)
print(datetime.date.fromtimestamp(13467891).month)
print(datetime.date.fromtimestamp(13467891).day)