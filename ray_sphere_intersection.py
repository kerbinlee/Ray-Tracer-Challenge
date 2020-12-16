from canvas import Canvas
from color import Color
from intersection import Intersection
from ray import Ray
from sphere import Sphere
from transformations import Transformations
from tuple import *

import math

if __name__ == '__main__':
    ray_origin = Point(0, 0, -5)

    wall_z = 10
    wall_size = 15

    canvas_pixels = 100
    pixel_size = wall_size / canvas_pixels

    half = wall_size / 2

    canvas = Canvas(canvas_pixels, canvas_pixels)
    color = Color(1, 0, 0)
    shape = Sphere()
    
    for y in range(canvas_pixels):
        world_y = half - pixel_size * y

        for x in range(canvas_pixels):
            world_x = -half + pixel_size * x

            position = Point(world_x, world_y, wall_z)

            r = Ray(ray_origin, Tuple.normalize(position - ray_origin))
            # shrink along y-axis
            # r = r.transform(Transformations.scaling(1, 0.5, 1))

            # shrink along x-axis
            # r = r.transform(Transformations.scaling(0.5, 1, 1))

            # shrink and rotate
            # r = r.transform(Transformations.rotation_z(math.pi / 4)).transform(Transformations.scaling(0.5, 1, 1))

            # shrink and skew
            # r = r.transform(Transformations.shearing(1, 0, 0, 0, 0, 0)).transform(Transformations.scaling(0.5, 1, 1))

            xs = shape.intersect(r)

            if Intersection.hit(xs) is not None:
                canvas.write_pixel(x, y, color)

    canvas.canvas_to_ppm()
