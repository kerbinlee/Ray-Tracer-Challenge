from bounds import Bounds
from intersection import Intersection
from ray import Ray
from shape import Shape
from tuple import *
from typing import Iterable, Tuple as PythonTuple

class Cube(Shape):
    def __init__(self):
        super().__init__()
    
    def __eq__(self, other):
        return super().__eq__(other)

    def local_intersect(self, ray: Ray) -> Iterable[Intersection]:
        xtmin, xtmax = Cube.check_axis(ray.origin.x, ray.direction.x)
        ytmin, ytmax = Cube.check_axis(ray.origin.y, ray.direction.y)
        ztmin, ztmax = Cube.check_axis(ray.origin.z, ray.direction.z)

        tmin = max([xtmin, ytmin, ztmin])
        tmax = min([xtmax, ytmax, ztmax])

        if tmin > tmax:
            return []
        
        return [Intersection(tmin, self), Intersection(tmax, self)]

    def local_normal_at(self, local_point: Point = None) -> Vector:
        maxc = max([abs(local_point.x), abs(local_point.y), abs(local_point.z)])

        if maxc == abs(local_point.x):
            return Vector(local_point.x, 0, 0)
        elif maxc == abs(local_point.y):
            return Vector(0, local_point.y, 0)
        return Vector(0, 0, local_point.z)

    def check_axis(origin: float, direction: float, min_axis_value: float = -1, max_axis_value: float = 1) -> PythonTuple[float, float]:
        tmin_numerator = (min_axis_value - origin)
        tmax_numerator = (max_axis_value - origin)

        if abs(direction) >= Constants.epsilon:
            tmin = tmin_numerator / direction
            tmax = tmax_numerator / direction
        else:
            tmin = tmin_numerator * math.inf
            tmax = tmax_numerator * math.inf

        if tmin > tmax:
            tmin, tmax = tmax, tmin

        return tmin, tmax

    def bounds_of(self) -> Bounds:
        min = Point(-1, -1, -1)
        max = Point(1, 1, 1)
        return Bounds(min, max)
        