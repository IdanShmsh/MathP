import math
from _math import graphics_engine

renderer = graphics_engine.renderer().init(name="main", fps = 30, width=1080 / 2, height=1920 / 2)

renderer.set_camera_position((0, 2.5, -5))
renderer.set_camera_angles((0, 0, 0))
renderer.set_camera_fov(math.pi / 2)

def increaseCamAngle():
    a = renderer.camera_angles[1] - 0.01

    renderer.set_camera_position((5 * math.sin(a), (2.5 * (math.sin(2* a) ** 2) + 1), -5 * math.cos(a)))

    renderer.set_camera_angles((0, a, 0))

renderer.sign_to_update(increaseCamAngle)

renderer.create_3d_axis()

renderer.draw_world_line((-1, 1, 1), (1, 1, 1))
renderer.draw_world_line((1, -1, 1), (1, 1, 1))
renderer.draw_world_line((1, 1, -1), (1, 1, 1))
renderer.draw_world_line((1, -1, -1), (-1, -1, -1))
renderer.draw_world_line((-1, 1, -1), (-1, -1, -1))
renderer.draw_world_line((-1, -1, 1), (-1, -1, -1))
renderer.draw_world_line((-1, 1, 1), (-1, 1, -1))
renderer.draw_world_line((-1, 1, 1), (-1, -1, 1))
renderer.draw_world_line((1, -1, 1), (-1, -1, 1))
renderer.draw_world_line((1, -1, 1), (1, -1, -1))
renderer.draw_world_line((1, 1, -1), (1, -1, -1))
renderer.draw_world_line((1, 1, -1), (-1, 1, -1))

renderer.draw_world_line((-1, 4, 1), (1, 4, 1))
renderer.draw_world_line((1, 2, 1), (1, 4, 1))
renderer.draw_world_line((1, 4, -1), (1, 4, 1))
renderer.draw_world_line((1, 2, -1), (-1, 2, -1))
renderer.draw_world_line((-1, 4, -1), (-1, 2, -1))
renderer.draw_world_line((-1, 2, 1), (-1, 2, -1))
renderer.draw_world_line((-1, 4, 1), (-1, 4, -1))
renderer.draw_world_line((-1, 4, 1), (-1, 2, 1))
renderer.draw_world_line((1, 2, 1), (-1, 2, 1))
renderer.draw_world_line((1, 2, 1), (1, 2, -1))
renderer.draw_world_line((1, 4, -1), (1, 2, -1))
renderer.draw_world_line((1, 4, -1), (-1, 4, -1))