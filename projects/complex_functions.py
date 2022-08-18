import math
import sys

import numpy as np
from PIL import Image
import _math.complex_numbers as cn

class grapher:

    def __init__(self, name="", rangeX=(-50,50), rangeY=(-50,50), accuracy=0.01, func=None):
        self.rangeX=rangeX
        self.rangeY=rangeY
        self.accuracy = accuracy
        self.func = func
        self.name = name

    def set_func(self, func):
        self.func = func

    def graph(self,calc_range_X, calc_range_Y, accuracy):

        graph_name = (self.name + "-[" + str(self.rangeX) + "," + str(self.rangeY) +
                      "]-calc[" + str(calc_range_X) + "," + str(calc_range_Y) + "]-acc" + str(accuracy))
        graph_name = graph_name.replace(".", ",")

        w = int((self.rangeX[1] - self.rangeX[0]) / self.accuracy)
        h = int((self.rangeY[1] - self.rangeY[0]) / self.accuracy)

        pixels = np.zeros((w, h, 3), dtype=np.uint8)

        rX = int((calc_range_X[1] - calc_range_X[0]) / accuracy)
        rY = int((calc_range_Y[1] - calc_range_Y[0]) / accuracy)

        i = 0

        for x in range(rX):
            for y in range(rY):
                a = (x * accuracy) + calc_range_X[0]
                b = (y * accuracy) + calc_range_Y[0]

                num = self.func(complex(a, b))

                X = int(w * (num.real - self.rangeX[0]) / (self.rangeX[1] - self.rangeX[0]))
                Y = h - int(h * (num.imag - self.rangeY[0]) / (self.rangeY[1] - self.rangeY[0]))

                if 1 <= X < w - 1 and 1 <= Y < h - 1:
                    _a = 4 * ((abs(a - math.floor(a)) - 0.5) ** 2)
                    _b = 4 * ((abs(b - math.floor(b)) - 0.5) ** 2)
                    _c = math.sqrt(_a * _b)
                    pixels[X + 1][Y] = pixels[X - 1][Y] = pixels[X][Y + 1] = pixels[X][Y - 1] = (_b * 150, _a * 255, _b * 255)
                    pixels[X][Y] = (_c * 255, _c * 255, _c * 255)
                i += 1

                sys.stdout.write("\rrendering " + str(i) + "/" + str(rX*rY) + " [" + str(int((100 * i) / (rX*rY))) + "%]")

        img = Image.fromarray(pixels, 'RGB')
        img = img.transpose(5)

        save_file = "outputs/complex_graphs/" + graph_name + ".jpeg"
        img.save(save_file, quality=100)
        img.show()

sqrt_5 = math.sqrt(5)
phi = (1 + sqrt_5) * 0.5
_phi = (1 - sqrt_5) * 0.5

def Fibonacci(z):
    n = ((phi ** z) - (_phi ** z)) / sqrt_5
    return n

def zeta(z, A):
    sum = 0
    for i in range(1, A):
        sum = sum + (1 / (i ** z))
    return sum

def sin(z,A):
    sum = 0
    for i in range(A):
        sum += ((((-1) ** i) / math.factorial((2*i) + 1)) * (z ** ((2*i) + 1)))
    return sum

def FUNC(z):
    return sin(z, 50)

grapher(name="Sin", rangeX=(-5, 5), rangeY=(-5, 5), accuracy=0.01,func=FUNC).graph((-10, 10), (-10, 10), 0.01)

while True:
    pass