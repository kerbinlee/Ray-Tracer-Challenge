from shape import Shape
from intersection import Intersection
from ray import Ray
from shape import Shape
from tuple import *
from typing import Iterable

import math

class Sphere(Shape):
    def __init__(self):
        super().__init__()
        self.origin: Point = Point(0, 0, 0)
        self.radius: float = 1
    
    def __eq__(self, other):
        return super().__eq__(other) and self.origin == other.origin and self.radius == other.radius

    def intersect(self, ray: Ray) -> Iterable[Intersection]:
        super().intersect(ray)
        sphere_to_ray = self._local_ray.origin - Point(0, 0, 0)
        a = Vector.dot(self._local_ray.direction, self._local_ray.direction)
        b = 2 * Vector.dot(self._local_ray.direction, sphere_to_ray)
        c = Vector.dot(sphere_to_ray, sphere_to_ray) - 1
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return Intersection.intersections()

        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)

        return Intersection.intersections(Intersection(t1, self), Intersection(t2, self))

    def local_normal_at(self, local_point: Point) -> Vector:
        super().local_normal_at(local_point)
        return Vector(local_point.x, local_point.y, local_point.z)
