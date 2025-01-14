# Write a Python program to generate 26 text files
# named A.txt, B.txt, and so on up to Z.txt.

import os
import string_lesson

if not os.path.exists('D:/file2'):
    os.makedirs('D:/file2')

for letter in string.ascii_uppercase:
   with open(letter + ".txt", "w") as f:
       f.writelines(letter)

print('-----')

import os

def generate_text_files():
    # Get the current working directory
    current_directory = os.getcwd()

    # Create a directory named 'text_files' if it doesn't exist
    directory_path = os.path.join(current_directory, 'text_files')
    os.makedirs(directory_path, exist_ok=True)

    # Generate text files A.txt to Z.txt
    for char_code in range(ord('A'), ord('Z') + 1):
        file_name = f"{chr(char_code)}.txt"
        file_path = os.path.join(directory_path, file_name)

        # Create and write to the text file
        with open(file_path, 'w') as file:
            file.write(f"This is the content of {file_name}")

    print("Text files generated successfully in the 'text_files' directory.")

if __name__ == "__main__":
    generate_text_files()
