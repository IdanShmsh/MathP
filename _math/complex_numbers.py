import math

class complex_number:

    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b
        self.update_polar()

    def __str__(self):
        A = ""
        B = ""
        if self.a != 0:
            A = str(self.a)

        if self.b > 0:
            B = " + " + str(self.b) + "i"
        elif self.b < 0:
            B = " - " + (str(self.b)[1:]) + "i"

        return A + B



    def set_a(self, a):
        self.a = a
        self.update_polar()

    def set_b(self, b):
        self.b = b
        self.update_polar()

    def set_theta(self, t):
        self.theta = t
        self.update_cartesian()

    def set_r(self, r):
        self.r = r
        self.update_cartesian()

    def update_polar(self):

        if self.a == 0:
            if self.b > 0:
                self.theta = math.pi / 2
            elif self.b > 0:
                self.theta = -math.pi / 2
            else:
                self.theta = 0
        else:
            self.theta = math.atan(self.b / self.a)

        self.theta = self.theta % (2 * math.pi)
        self.r = math.sqrt((self.b*self.b) + (self.a*self.a))

    def update_cartesian(self):
        self.a = self.r * math.cos(self.theta)
        self.b = self.r * math.sin(self.theta)

    @staticmethod
    def cis(theta):
        num = complex_number()
        num.theta = theta
        num.r = 1
        num.update_cartesian()
        return num

    def add(self, other):

        a = self.a + other.a
        b = self.b + other.b

        num = complex_number(a, b)
        num.update_polar()

        return num

    def sub(self, other):

        a = self.a - other.a
        b = self.b - other.b

        num = complex_number(a, b)
        num.update_polar()

        return num

    def mult(self, other):

        a = (self.a * other.a) - (self.b * other.b)
        b = (self.a * other.b) + (self.b * other.a)

        num = complex_number(a, b)
        num.update_polar()

        return num

    def dev(self, other):

        a = ((self.a * other.a) + (self.b * other.b)) / ((other.a ** 2) + (other.b ** 2))
        b = ((self.b * other.a) - (self.a * other.b)) / ((other.a ** 2) + (other.b ** 2))

        num = complex_number(a, b)
        num.update_polar()

        return num

    def pow(self, A):
        A = A % (2*math.pi)
        num1 = complex_number((A ** self.a), 0)
        if A == 0:
            A = 2*math.pi
        num2 = complex_number.cis(math.log(A) * self.b)

        return num1.mult(num2)

    def to_the(self, A):

        numP = complex_number.cis(A*self.theta)
        R = self.r ** A

        return complex_number(numP.a * R, numP.b * R)
