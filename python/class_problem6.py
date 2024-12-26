# Write a Python program to create a class representing a Circle.
# calculate its area and perimeter.


class calculate:
    def __init__(self, pi, r):
        self.pi = pi
        self.r = r
        print('the area and perimeter area: ')

class area(calculate):
    def __init__(self, pi, r):
        super().__init__(pi, r)
        ar = pi * pow(r, 2)
        print(ar)

class perimeter(area):
    def __init__(self, pi, r):
        area.__init__(self, pi, r)
        peri = 2 * pi * r
        print(peri)

cal = perimeter(3.1416, 3)

