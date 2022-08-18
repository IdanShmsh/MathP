import colorsys
import random
import threading
import time
from winsound import Beep
import tools.graphics as g

class sorter:
    finished = False

    def __init__(self, v_arr):
        self.v_arr = v_arr

    def main_algo(self):
        return  # do nothing


class non_sorter(sorter):
    current_index = 0

    def main_algo(self):
        self.current_index = self.current_index + 1
        if self.current_index >= len(self.v_arr.array):
            self.current_index = 0
        self.v_arr.get_value(self.current_index)


class bubble_sort(sorter):

    def main_algo(self):
        for i in range(self.v_arr.size):
            for j in range(self.v_arr.size - 1 - i):
                v1 = self.v_arr.get_value(j)
                v2 = self.v_arr.get_value(j + 1)

                if v1 > v2:
                    self.v_arr.set_value(j, v2)
                    self.v_arr.set_value(j + 1, v1)

        for i in range(self.v_arr.size):
            self.v_arr.get_value(i)

class quick_sort(sorter):

    def main_algo(self):
        self.sort_recu()

    def sort_recu(self, s = 0, e = None):
        if e == None:
            e = self.v_arr.size - 1
        if s < e:
            p = self.partition(s, e)
            self.sort_recu(s, p - 1)
            self.sort_recu(p + 1, e)

    def partition(self, s, e):
        pivot = self.v_arr.get_value(e)
        i = s
        for j in range(s, e):
            v1 = self.v_arr.get_value(j)
            if v1 <= pivot:
                v2 = self.v_arr.get_value(i)
                self.v_arr.set_value(j,v2)
                self.v_arr.set_value(i,v1)
                i += 1
        v1 = self.v_arr.get_value(i)
        v2 = self.v_arr.get_value(e)
        self.v_arr.set_value(e,v1)
        self.v_arr.set_value(i,v2)
        return i


class visualized_array:

    def __init__(self, size, stick_thickness=5):

        self.size = size

        self.stick_thickness = stick_thickness

        self.array = [i for i in range(size)]

        random.shuffle(self.array)

        self.display = g.GraphWin("sort", size * stick_thickness, size)

        self.sorter = None

        self.display.setBackground(g.color_rgb(0, 0, 0))

        self.lines = [None for i in range(size)]
        self.pointer = None

        for i in range(size):
            value = self.array[i]
            l = g.Line(g.Point(self.stick_thickness * (i + 0.5), len(self.array)),
                       g.Point(self.stick_thickness * (i + 0.5), len(self.array) - value))
            l.setFill(self.value_to_color(value))
            l.setWidth(self.stick_thickness)
            self.lines[i] = l.draw(self.display)

    def get_value(self, index):
        value = self.array[index]

        def visual():
            threading.Thread(target=self.use_sound, args=(self.value_to_tone(value),)).start()

            if self.pointer:
                self.pointer.undraw()

            l = g.Line(
                g.Point(self.stick_thickness * (index + 0.5), len(self.array)),
                g.Point(self.stick_thickness * (index + 0.5), len(self.array) - self.array[index])
            )
            l.setFill(g.color_rgb(255, 255, 255))
            l.setWidth(self.stick_thickness)
            self.pointer = l.draw(self.display)

            self.lines[index].undraw()

            l = g.Line(
                g.Point(self.stick_thickness * (index + 0.5), len(self.array)),
                g.Point(self.stick_thickness * (index + 0.5), len(self.array) - value)
            )
            l.setFill(self.value_to_color(value))
            l.setWidth(self.stick_thickness)
            self.lines[index] = l.draw(self.display)

        visual()

        return value

    def set_value(self, index, value):
        def visual():
            threading.Thread(target=self.use_sound, args=(self.value_to_tone(value),)).start()

            if self.pointer:
                self.pointer.undraw()

            l = g.Line(
                g.Point(self.stick_thickness * (index + 0.5), len(self.array)),
                g.Point(self.stick_thickness * (index + 0.5), len(self.array) - self.array[index])
            )
            l.setFill(g.color_rgb(255, 255, 255))
            l.setWidth(self.stick_thickness)
            self.pointer = l.draw(self.display)

            self.lines[index].undraw()

            l = g.Line(
                g.Point(self.stick_thickness * (index + 0.5), len(self.array)),
                g.Point(self.stick_thickness * (index + 0.5), len(self.array) - value)
            )
            l.setFill(self.value_to_color(value))
            l.setWidth(self.stick_thickness)
            self.lines[index] = l.draw(self.display)

        visual()

        self.array[index] = value

        return value

    def value_to_tone(self, value):
        low_freq = 250
        high_freq = 500
        return int(low_freq + (((value) / len(self.array)) * (high_freq - low_freq)))

    def value_to_color(self, value):
        color = colorsys.hsv_to_rgb(value / len(self.array), 1, 1)
        color = g.color_rgb(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
        return color

    def use_sound(self, hz):
        Beep(hz, 100)

    def show_off(self):
        for i in range(self.size):
            self.get_value(i)
            time.sleep(0.01)


arr = visualized_array(size=500, stick_thickness=2)
quick_sort(arr).main_algo()
arr.show_off()

while True:
    pass
