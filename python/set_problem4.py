# Write a Python program to find all the unique words and
# count the frequency of occurrence from a given list of strings.
# Use Python set data type.
def count_unique_words(strings):
    word_count = {}

    for string in strings:
        # Split the string into words
        words = string.split()

        for word in words:
            # Remove any punctuation from the word and convert it to lowercase
            word = word.strip('.,?!').lower()

            # If the word is not empty after removing punctuation, count it
            if word:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

    return word_count


# Example usage
strings = [
    "This is a sample string.",
    "Another sample string with words.",
    "This is a third string with unique words.",
]

word_count = count_unique_words(strings)

for word, count in word_count.items():
    print(f"{word}: {count}")
