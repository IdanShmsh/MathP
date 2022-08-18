import sys

import numpy as np

import _math.complex_numbers as cn
from PIL import Image
import matplotlib.pyplot as plt

class mendlebrot_set:

    def __init__(self, rangeX=(-2,0.5), rangeY=(0, 1.5), accuracy=0.0001, cpd=100):

        self.rangeX = rangeX
        self.rangeY = rangeY

        self.accuracy = accuracy

        self.cpd=cpd

        self.iteration = 0

        self.renderer = None

    def render_visual(self):

        w = round(abs(self.rangeX[1] - self.rangeX[0]) / self.accuracy)
        h = round(abs(self.rangeY[1] - self.rangeY[0]) / self.accuracy)

        print("render size: width=" + str(w) + ", height=" + str(h))

        pixels = np.zeros((w, h, 3), dtype=np.uint8)

        i = 0
        x = self.rangeX[0]
        while x <= self.rangeX[1]:
            y = self.rangeY[0]
            while y <= self.rangeY[1]:
                c = cn.complex_number(a=x, b=y)
                brt = self.get_mandle_co(c)

                pX = int((x - self.rangeX[0]) / self.accuracy)
                pY = h - int((y - self.rangeY[0]) / self.accuracy)

                if pY < h and pX < w:
                    pixels[pX, pY] = [brt * 255,brt * brt * brt * 255,brt * 255]

                y += self.accuracy
                i += 1

                sys.stdout.write("\rrendering" + str(i) + "/" + str(w*h) + " [" + str(int((100 * i) / (w * h)))+ "%]")
            x += self.accuracy

        img = Image.fromarray(pixels, 'RGB')
        img = img.transpose(5)

        save_file = "outputs/mandlebrot/a=" + (str(self.accuracy)).replace(".", ",") + "rX=" + str(self.rangeX) + "rY=" + str(self.rangeY) + ".jpeg"
        img.save(save_file, quality=100)
        img.show()


    def get_mandle_co(self, c):
        z = cn.complex_number()

        prev_radius = c.r

        itt = 0
        for i in range(self.cpd):
            z = z.mult(z)
            z = z.add(c)
            itt = i
            if z.r > 4:
                break

        return itt / self.cpd

m = mendlebrot_set()
m.render_visual()