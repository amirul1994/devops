# Write a Python program to find the list of words that are longer
# than n from a given list of words.

def word_length(my_list, n):
    for word in my_list:
        if len(word) > n:
            print(word)


word_length(['imam', 'muhammad', 'amirul', 'maula'],4)