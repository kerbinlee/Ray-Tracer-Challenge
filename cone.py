from bounds import Bounds
from revolved_plane import RevolvedPlane
from intersection import Intersection
from ray import Ray
from tuple import *
from typing import Iterable

class Cone(RevolvedPlane):
    def __init__(self):
        super().__init__()
    
    def __eq__(self, other):
        return super().__eq__(other)

    def local_intersect(self, ray: Ray) -> Iterable[Intersection]:
        a = ray.direction.x ** 2 - ray.direction.y ** 2 + ray.direction.z ** 2
        b = 2 * ray.origin.x * ray.direction.x - 2 * ray.origin.y * ray.direction.y + 2 * ray.origin.z * ray.direction.z

        if abs(a) < Constants.epsilon and abs(b) < Constants.epsilon:
            return []

        c = ray.origin.x ** 2 - ray.origin.y ** 2 + ray.origin.z ** 2

        # ray is parallel to the y axis
        if abs(a) < Constants.epsilon and abs(b) > Constants.epsilon:
            xs = [Intersection(-c / (2 * b), self)]
            Cone.intersect_caps(self, ray, xs)
            return xs

        xs = self.find_intersections(ray, a, b, c)

        Cone.intersect_caps(self, ray, xs)

        return xs

    def local_normal_at_wall(self, local_point: Point) -> Vector:
            y = math.sqrt(local_point.x ** 2 + local_point.z ** 2)
            if local_point.y > 0:
                y = -y
            return Vector(local_point.x, y, local_point.z)

    def local_intersect_caps(self: 'Cone', ray: Ray, xs: Iterable[Intersection], t0, t1) -> None:
        if Cone.check_cap(ray, t0, self.minimum):
            xs.append(Intersection(t0, self))

        if Cone.check_cap(ray, t1, self.maximum):
            xs.append(Intersection(t1, self))

    def bounds_of(self) -> Bounds:
        a = abs(self.minimum)
        b = abs(self.maximum)
        limit = max(a, b)

        return Bounds(Point(-limit, self.minimum, -limit), Point(limit, self.maximum, limit))  
        