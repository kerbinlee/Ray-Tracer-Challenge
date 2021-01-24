from intersection import Intersection
from ray import Ray
from shape import Shape
from tuple import *
from typing import Iterable

class Plane(Shape):
    def __init__(self):
        super().__init__()
        self.origin: Point = Point(0, 0, 0)
        self.radius: float = 1
    
    def __eq__(self, other):
        return super().__eq__(other) and self.origin == other.origin and self.radius == other.radius

    def intersect(self, ray: Ray) -> Iterable[Intersection]:
        if abs(ray.direction.y) < Constants.epsilon:
            return []

        t = -ray.origin.y / ray.direction.y
        return [Intersection(t, self)]

    def local_normal_at(self, local_point: Point = None) -> Vector:
        return Vector(0, 1, 0)
