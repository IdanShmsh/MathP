import math
import transformations
import pygame
import threading
import numpy as np

running_renderers = {}


class renderer:
    background_color = (0, 0, 0)  # black

    def init(self, name="main", fps=30, height=1080, width=1920):

        if name in running_renderers:
            return running_renderers[name]

        # initialize it
        pygame.init()

        self.name = name

        # configurations
        self.frames_per_second = fps
        self.window_height = height
        self.window_height_half = height / 2
        self.window_width = width
        self.window_width_half = width / 2
        self.screen_scale = 1
        self.rangeX = (-5, 5)
        self.rangeY = (-5, 5)

        self.camera_position = (0, 0, 0)
        self.camera_angles = (math.pi / 2, 0, 0)
        self.camera_fov = math.pi / 2
        self.camera_quaternion = []
        self.camera_matrix = np.matrix([])

        # creating window
        self.display = pygame.display.set_mode((self.window_width, self.window_height))

        self.data = []

        self.update_signed_funcs = []

        # self.start_update()
        threading.Thread(target=self.start_update).start()

        running_renderers[name] = self
        return self

    def start_update(self):
        # creating our frame regulator
        clock = pygame.time.Clock()
        flag = True

        # forever loop
        while flag:
            clock.tick(self.frames_per_second)

            self.display.fill(self.background_color)

            for f in self.update_signed_funcs:
                f()

            self.draw_data()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    def draw_data(self):
        for d in self.data:
            if d[0] == "world_point":
                args = d[1]
                pixel = self.project_point_to_screen(args[1])
                if pixel:
                    pygame.draw.circle(self.display, args[0], pixel, args[2])
            elif d[0] == "world_line":
                args = d[1]
                pixel1 = self.project_point_to_screen(args[1])
                pixel2 = self.project_point_to_screen(args[2])
                if pixel1 and pixel2:
                    pygame.draw.line(self.display, args[0], pixel1, pixel2, args[3])

    def set_camera_position(self, point):
        self.camera_position = point
        self.update_camera_matrix()

    def set_camera_angles(self, angles):
        self.camera_angles = angles
        self.update_camera_matrix()

    def set_camera_fov(self, fov):
        self.camera_fov = fov

    def update_camera_matrix(self):
        phi = self.camera_angles[0]
        theta = self.camera_angles[1]
        psy = self.camera_angles[2]
        self.camera_quaternion = [
            (math.cos(phi / 2) * math.cos(theta / 2) * math.cos(psy / 2)) + (
                        math.sin(phi / 2) * math.sin(theta / 2) * math.sin(psy / 2)),
            (math.sin(phi / 2) * math.cos(theta / 2) * math.cos(psy / 2)) - (
                        math.cos(phi / 2) * math.sin(theta / 2) * math.sin(psy / 2)),
            (math.cos(phi / 2) * math.sin(theta / 2) * math.cos(psy / 2)) + (
                        math.sin(phi / 2) * math.cos(theta / 2) * math.sin(psy / 2)),
            (math.cos(phi / 2) * math.cos(theta / 2) * math.sin(psy / 2)) - (
                        math.sin(phi / 2) * math.sin(theta / 2) * math.cos(psy / 2))
        ]
        q = self.camera_quaternion
        r = 0
        x = 1
        y = 2
        z = 3
        self.camera_matrix = np.matrix([
            [1 - (2 * ((q[y] ** 2) + (q[z] ** 2))), 2 * ((q[x] * q[y]) - (q[z] * q[r])),
             2 * ((q[x] * q[z]) + (q[y] * q[r])), 0],
            [2 * ((q[x] * q[y]) + (q[z] * q[r])), 1 - (2 * ((q[x] ** 2) + (q[z] ** 2))),
             2 * ((q[y] * q[z]) - (q[x] * q[r])), 0],
            [2 * ((q[x] * q[z]) - (q[y] * q[r])), 2 * ((q[y] * q[z]) + (q[x] * q[r])),
             1 - (2 * ((q[x] ** 2) + (q[y] ** 2))), 0],
            [self.camera_position[0], self.camera_position[1], self.camera_position[2], 1]
        ])

    def project_point_to_screen(self, point):

        pVector = np.matrix([[point[0], point[1], point[2], 1]])

        localP = (pVector.dot(self.camera_matrix ** -1))

        temp = []
        for i in range(0, 4):
            temp.append(localP[0, i])

        localP = temp

        if (localP[2] <= 0):
            return None

        minDim = min([self.window_height, self.window_width])
        sX = self.window_width_half - ((minDim * 0.5 * localP[0]) / (localP[2] * math.tan(self.camera_fov / 2)))
        sY = self.window_height_half - ((minDim * 0.5 * localP[1]) / (localP[2] * math.tan(self.camera_fov / 2)))

        return (sX, sY)

    def set_background(self, color):
        background_color = color

    def draw_world_point(self, point, color=(255, 255, 255), radius=1):
        self.data.append(("world_point", (color, point, radius)))

    def draw_world_line(self, point1, point2, color=(255, 255, 255), thickness=1):
        self.data.append(("world_line", (color, point1, point2, thickness)))

    def set_screen_scale(self, scale):
        self.screen_scale = scale

    def sign_to_update(self, func):
        self.update_signed_funcs.append(func)

    def center_point(self, point):
        return (point[0] + (self.window_width_half),
                point[1] + (self.window_height_half))

    def create_3d_axis(self, rangeX=(-5, 5), rangeY=(-5, 5), rangeZ=(-5, 5)):
        self.draw_world_line((rangeX[0], 0, 0), (rangeX[1], 0, 0), (255, 0, 0), 5)
        self.draw_world_line((0, rangeY[0], 0), (0, rangeY[1], 0), (0, 255, 0), 5)
        self.draw_world_line((0, 0, rangeZ[0]), (0, 0, rangeZ[1]), (0, 0, 255), 5)

    def set_screen_2d_range(self, rangeX, rangeY):
        self.rangeX = rangeX
        self.rangeY = rangeY

    def transform_pixel(self, pixel):

        pixel = (self.window_width * ((pixel[0] - self.rangeX[0]) / (self.rangeX[1] - self.rangeX[0])),
                 self.window_width * ((pixel[1] - self.rangeY[0]) / (self.rangeY[1] - self.rangeY[0])))

        pixel = (self.window_width_half + ((pixel[0] - self.window_width_half) * self.screen_scale),
                 self.window_height_half + ((pixel[1] - self.window_height_half) * self.screen_scale))

        return pixel


class Graphing:
    def __init__(self):
        pass
