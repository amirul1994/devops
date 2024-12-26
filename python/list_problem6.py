#  Write a Python function that takes two lists and returns True
#  if they have at least one common member.

def sim(my_list1, my_list2):
    for i in my_list1:
        if i in my_list2:
            print("found")
            return True


sim([1, 2, 3, 4, 5], [5, 6, 7, 8, 9])
sim([1, 2, 3, 4, 5, 6], [5, 6, 7, 8, 9])
sim([1, 2, 3, 4], [5, 6, 7, 8, 9])