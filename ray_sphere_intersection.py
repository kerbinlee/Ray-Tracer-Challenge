from canvas import Canvas
from color import Color
from intersection import Intersection
from light import PointLight
from material import Material
from ray import Ray
from sphere import Sphere
from transformations import Transformations
from tuple import *

import math

if __name__ == '__main__':
    ray_origin = Point(0, 0, -5)

    wall_z = 10
    wall_size = 7

    canvas_pixels = 100
    pixel_size = wall_size / canvas_pixels

    half = wall_size / 2

    canvas = Canvas(canvas_pixels, canvas_pixels)
    color = Color(1, 0, 0)
    shape = Sphere()
    shape.material = Material()
    shape.material.color = Color(1, 0.2, 1)

    light_position = Point(-10, 10, -10)
    light_color = Color(1, 1, 1)
    light = PointLight(light_position, light_color)
    
    for y in range(canvas_pixels):
        world_y = half - pixel_size * y

        for x in range(canvas_pixels):
            world_x = -half + pixel_size * x

            position = Point(world_x, world_y, wall_z)

            r = Ray(ray_origin, Vector.normalize(position - ray_origin))
            # shrink along y-axis
            # r = r.transform(Transformations.scaling(1, 0.5, 1))

            # shrink along x-axis
            # r = r.transform(Transformations.scaling(0.5, 1, 1))

            # shrink and rotate
            # r = r.transform(Transformations.rotation_z(math.pi / 4)).transform(Transformations.scaling(0.5, 1, 1))

            # shrink and skew
            # r = r.transform(Transformations.shearing(1, 0, 0, 0, 0, 0)).transform(Transformations.scaling(0.5, 1, 1))

            xs = shape.intersect(r)

            hit = Intersection.hit(xs)
            if hit is not None:
                point = Ray.position(r, hit.t)
                normal = shape.normal_at(point)
                eye = -r.direction
                color = PointLight.lighting(hit.object.material, hit.object, light, point, eye, normal, False)
                canvas.write_pixel(x, y, color)

    canvas.canvas_to_ppm()
