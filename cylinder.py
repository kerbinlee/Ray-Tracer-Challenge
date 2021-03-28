from bounds import Bounds
from intersection import Intersection
from ray import Ray
from revolved_plane import RevolvedPlane
from tuple import *
from typing import Iterable

class Cylinder(RevolvedPlane):
    def __init__(self):
        super().__init__()
    
    def __eq__(self, other):
        return super().__eq__(other)

    def local_intersect(self, ray: Ray) -> Iterable[Intersection]:
        a = ray.direction.x ** 2 + ray.direction.z ** 2

        # ray is parallel to the y axis
        if a < Constants.epsilon:
            xs = []
            Cylinder.intersect_caps(self, ray, xs)
            return xs

        b = 2 * ray.origin.x * ray.direction.x + 2 * ray.origin.z * ray.direction.z
        c = ray.origin.x ** 2 + ray.origin.z ** 2 - 1

        xs = self.find_intersections(ray, a, b, c)

        Cylinder.intersect_caps(self, ray, xs)

        return xs

    def local_normal_at_wall(self, local_point: Point = None) -> Vector:
        return Vector(local_point.x, 0, local_point.z)
    
    def local_intersect_caps(self: 'Cylinder', ray: Ray, xs: Iterable[Intersection], t0, t1) -> None:
        if Cylinder.check_cap(ray, t0, 1):
            xs.append(Intersection(t0, self))

        if Cylinder.check_cap(ray, t1, 1):
            xs.append(Intersection(t1, self))

    def bounds_of(self) -> Bounds:
        min = Point(-1, self.minimum, -1)
        max = Point(1, self.maximum, 1)
        return Bounds(min, max)
        