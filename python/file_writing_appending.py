a = open('test.txt', 'w')
a.write('this is another program')

b = open('D:/test.txt', 'w')
b.write('this is line 2\n this is line 3\n this is line 4')

b.writelines('this is a line\n this is another line')
b.write('this is a newly created line')

c = open('D:/test2.txt', 'a')
c.write('this is line 2')
c.write('\n this is line 3')

L = ['this is line 3\n', 'this is line 4\n', 'this is line 5']

with open('D:/test3.txt', 'a') as d:
    d.writelines(L)