import math

from bounds import Bounds
from intersection import Intersection
from ray import Ray
from shape import Shape
from tuple import *
from typing import Iterable

class Plane(Shape):
    def __init__(self):
        super().__init__()
    
    def __eq__(self, other):
        return super().__eq__(other)

    def local_intersect(self, ray: Ray) -> Iterable[Intersection]:
        if abs(ray.direction.y) < Constants.epsilon:
            return []

        t = -ray.origin.y / ray.direction.y
        return [Intersection(t, self)]

    def local_normal_at(self, local_point: Point = None, intersection: Intersection = None) -> Vector:
        return Vector(0, 1, 0)

    def bounds_of(self) -> Bounds:
        min = Point(-math.inf, 0, -math.inf)
        max = Point(math.inf, 0, math.inf)
        return Bounds(min, max)
