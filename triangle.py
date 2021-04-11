from bounds import Bounds
from intersection import Intersection
from ray import Ray
from shape import Shape
from tuple import *
from typing import Iterable

class Triangle(Shape):
    def __init__(self, p1: Point, p2: Point, p3: Point):
        super().__init__()
        self.p1: Point = p1
        self.p2: Point = p2
        self.p3: Point = p3
        self.e1: Vector = p2 - p1
        self.e2: Vector = p3 - p1
        self.normal: Vector = Vector.normalize(self.e2.cross(self.e1))
    
    def __eq__(self, other):
        return super().__eq__(other)

    def local_intersect(self, ray: Ray) -> Iterable[Intersection]:
        dir_cross_e2 = ray.direction.cross(self.e2)
        det = self.e1.dot(dir_cross_e2)
        if abs(det) < Constants.epsilon:
            return []

        f = 1.0 / det

        p1_to_origin = ray.origin - self.p1
        u = f * p1_to_origin.dot(dir_cross_e2)
        if u < 0 or u > 1:
            return []

        origin_cross_e1 = p1_to_origin.cross(self.e1)
        v = f * ray.direction.dot(origin_cross_e1)
        if v < 0 or (u + v) > 1:
            return []

        t = f * self.e2.dot(origin_cross_e1)
        return [Intersection(t, self, u, v)]

    def local_normal_at(self, local_point: Point = None, intersection: Intersection = None) -> Vector:
        return self.normal

    def bounds_of(self) -> Bounds:
        min = Point(-1, -1, -1)
        max = Point(1, 1, 1)
        return Bounds(min, max)
        