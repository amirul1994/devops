# Write a Python program to print all distinct
# values in a dictionary.
# Sample Data : [{"V":"S001"}, {"V": "S002"},
# {"VI": "S001"}, {"VI": "S005"}, {"VII":"S005"}, {"V":"S009"},{"VIII":"S007"}]

# Expected Output : Unique Values: {'S005', 'S002', 'S007',
# 'S001', 'S009'}

d1 = [{"V":"S001"}, {"V": "S002"}, {"VI": "S001"}, {"VI": "S005"},
      {"VII":"S005"}, {"V":"S009"},{"VIII":"S007"}]

my_list = []

for i in d1:
    #print(i)
    #print(i.values())
    value = list(i.values())
    print(value)

    if value not in my_list:
        my_list += value
        #my_list.append(value)

print((my_list))

s1 = set(my_list)
print(s1)