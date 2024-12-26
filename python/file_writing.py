with open('test_file.txt', 'w') as file:
    file.write("this is from our program")

with open('test_file.txt', 'a') as file:
    my_list = ['this is item 1\n', 'this is item 2\n', 'this '
                                                       'is item 3\n' ]
    file.write("this is from our program test\n")

    file.writelines(my_list)