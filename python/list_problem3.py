# Write a Python program to get a list, sorted in increasing order
# by the last element in each tuple from a given list of non-empty tuples.
# Sample List : [(2, 5), (1, 2), (4, 4), (2, 3), (2, 1)]
# Expected Result : [(2, 1), (1, 2), (2, 3), (4, 4), (2, 5)]


def last(n):
  print('this is ', n)
  return n[-1]

def sort_list_last(tuples):
  print('the tuples are', tuples)
  return sorted(tuples, key=last)
  # key needs a function to call

print(sort_list_last([(2, 5), (1, 2), (4, 4), (2, 3), (2, 1)]))


print('-------------')

sample_list = [(2, 5), (1, 2), (4, 4), (2, 3), (2, 1)]

# Sort the list based on the last element of each tuple
result = sorted(sample_list, key=lambda x: x[-1])

print("Sorted list in increasing order by the last element:")
print(result)