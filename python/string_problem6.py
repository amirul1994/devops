# Write a Python function that takes a list of words and
# return the longest word and the length of the longest one.
# Sample Output:
# Longest word: Exercises
# Length of the longest word: 9

def longest_word(my_list):
    value = []

    for i in my_list:
        value.append(len(i))

    #print(value)

    for i in my_list:
        if len(i) == max(value):
            print("the longest word is: {}".format(i))
            print("the length of the longest word is: ", len(i))
            print("-------------")


longest_word(['imam', 'muhammad', 'amirul', 'maula'])
longest_word(['chattogram', 'dhaka', 'rajshahi', 'khulna'])
