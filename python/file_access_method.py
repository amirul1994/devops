""" r - opens the file as read only; raises error if the file
doesn't exist

r+ - opens the file for both reading and writing; raises error
doesn't exist

w - opens the file as write only; if the file doesn't exist,
a new one gets created

w+ - opens the file for both reading and writing; the text is
overwritten and deleted from an existing file

a - opens the file for writing; creates one if the file doesn't
exist. The newly written data will be added at the end,
following the previously written data

a+ - opens the file for reading & writing; creates one if the
file doesn't exist. The newly written data will be added at the end,
following the previously written data
"""