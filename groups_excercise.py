import math

from camera import Camera
from color import Color
from cylinder import Cylinder
from group import Group
from light import PointLight
from sphere import Sphere
from transformations import Transformations
from tuple import *
from world import World


def hexagon_corner() -> Sphere:
    corner = Sphere()
    corner.transform = Transformations.translation(0, 0, -1).dot(Transformations.scaling(0.25, 0.25, 0.25))
    return corner

def hexagon_edge() -> Cylinder:
    edge = Cylinder()
    edge.minimum = 0
    edge.maximum = 1
    edge.transform = Transformations.translation(0, 0, -1).dot(Transformations.rotation_y(-math.pi / 6).dot(Transformations.rotation_z(-math.pi / 2).dot(Transformations.scaling(0.25, 1, 0.25))))
    return edge

def hexagon_side() -> Group:
    side = Group()
    side.add_child(hexagon_corner())
    side.add_child(hexagon_edge())
    return side

def hexagon() -> Group:
    hex = Group()
    for n in range(6):
        side = hexagon_side()
        side.transform = Transformations.rotation_y(n * math.pi / 3)
        hex.add_child(side)

    return hex

if __name__ == '__main__':
    hexagon = hexagon()

    # The light source is white, shining from above and to the left
    world = World()
    world.objects = [hexagon]
    world.light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))

    # Camera
    camera = Camera(200, 150, math.pi / 3)
    camera.transform = World.view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))

    # render the result to a canvas
    canvas = Camera.render(camera, world)
    canvas.canvas_to_ppm()
