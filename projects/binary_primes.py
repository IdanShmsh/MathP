import math
import sys

import numpy as np
from PIL import Image
import _math.primes as primes
import _math.binary as binary
import _math.complex_numbers as cn

def graph(count,image_scale=3):

    w = count * image_scale
    h = image_scale * int(math.log(count, 2) + 10)

    pixels = np.zeros((w, h, 3), dtype=np.uint8)

    def prime_run(p):
        global n
        try:
            n = n
        except:
            n = 0
        binary_digits = binary.to_binary_array(p)
        j = 0
        for i in range(len(binary_digits) - 1, -1, -1):
            d = binary_digits[j]
            for x in range(image_scale):
                for y in range(image_scale):
                    pixels[image_scale * n + x][image_scale * j + y] = (d * 255,d * 255,d * 255)
            j += 1
        n += 1
        sys.stdout.write("\rgenerating " + str(n) + "/" + str(count) + " [" + str(int((100 * n) / (count))) + "%]")

    primes.for_each_of_n(prime_run,count)

    img = Image.fromarray(pixels, 'RGB')
    img = img.transpose(5)

    save_file = "outputs/binary_primes/count=" + str(count) + ".jpeg"
    img.save(save_file, quality=100)
    img.show()

graph(1000, 15)

while True:
    pass