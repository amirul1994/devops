# Write a Python program that iterates the integers from 1 to 50. For multiples of three print "Fizz" instead of the number and for multiples of five print "Buzz". For numbers that are multiples of three and five, print "FizzBuzz".

for a in range(51):

  if a != 0:

    if a%3 == 0 and a%5 == 0:
      print('fizzbuzz')

    elif a%3 == 0:
     print('fizz')

    elif a%5 == 0:
     print('buzz')

    else:
       print(a)
