# 'time' is the module for time related operations
# the following syntax will import(load) the time module
import time

# time() will return the value in milliseconds passed from
# January 1, 1970
print(time.time())

# ctime() will return the current date & time
print(time.ctime())
print(type(time.ctime()))


# a process is a self-contained program running independently
# a thread is the smallest execution unit within a process
# multiple threads can run simultaneously
# threads share the same memory space and resources of a process
# but each thread has its own program counter, stack and
# registers

# key characteristics of thread
# concurrency, parallelism, thread states, thread sync
# thread creation, thread priorities, thread communication
# thread safety

# register is a small, temporary, high speed storage location
# within the cpu

# program counter is a register or memory location that
# keeps the track of the memory address
# of the next instruction to be executed in a program

# In programming, a stack is a linear data structure
# that follows the Last-In-First-Out (LIFO) principle,
# meaning that the last  item added to the stack
# is the first one to be removed.

# sleep() will halt the execution of a thread for
# a given number of seconds

print('i am new line')
time.sleep(2)
print('i am another line')

# localtime() returns the current time
print(time.localtime())
print(type(time.localtime()))

# if an argument is passed it will show the
# date according to it, the argument value is in milliseconds
print(time.localtime(1694509433.1394076))
print(time.localtime(1234567890))

import datetime

print(datetime.datetime.now())
print('utc time is', datetime.datetime.utcnow())
print(datetime.date.today())
print(datetime.date.fromtimestamp(12345678))
print(datetime.date.fromtimestamp(12345678).year)
print(datetime.date.fromtimestamp(12345678).month)
print(datetime.date.fromtimestamp(12345678).day)