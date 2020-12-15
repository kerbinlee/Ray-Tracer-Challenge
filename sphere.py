from intersection import Intersection
from tuple import *
from ray import Ray

import math

class Sphere:
    def __init__(self):
        self.origin: Point = Point(0, 0, 0)
        self.radius = 1

    def intersect(self, ray: Ray):
        sphere_to_ray = ray.origin - Point(0, 0, 0)
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return Intersection.intersections()

        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)

        return Intersection.intersections(Intersection(t1, self), Intersection(t2, self))
