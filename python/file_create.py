user_data = [
    {
        'file_name': 'user_1.txt',
        'context': "hello this is from User 1"
    },

    {
        'file_name': 'user_2.txt',
        'context': "hello this is from User 2"
    },

    {
        'file_name': 'user_3.txt',
        'context': "hello this is from User 3"
    }
]

with open('test_file_2.txt', 'w') as file:
    file.write("this is a test")
    #file.writelines(user_data)
    file.writelines(user_data[0])
    #file.writelines(user_data[0].file_name)
    # file.write(user_data[0].file_name)
    file.write(user_data[0]['file_name'])
