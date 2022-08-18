import math


def to_binary_array(x):
    size = int(math.log(x, 2) + 1)

    digits = []
    for i in range(size):
        digits.append(x % 2)
        x = int(x / 2)

    digits.reverse()

    return digits