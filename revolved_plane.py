from abc import abstractmethod
from intersection import Intersection
from ray import Ray
from shape import Shape
from tuple import *
from typing import Iterable

import math

class RevolvedPlane(Shape):
    def __init__(self):
        super().__init__()
        self.minimum: float = -math.inf
        self.maximum: float = math.inf
        self.closed:bool = False
    
    def __eq__(self, other):
        return super().__eq__(other) and self.minimum == other.minimum and self.maximum == other.maximum and self.closed == other.closed

    @abstractmethod
    def local_intersect(self, ray: Ray) -> Iterable[Intersection]:
        pass

    def local_normal_at(self, local_point: Point = None) -> Vector:
        # compute the square of the distance from the y axis
        dist = local_point.x ** 2 + local_point.z ** 2

        if dist < 1 and local_point.y >= self.maximum - Constants.epsilon:
            return Vector(0, 1, 0)
        elif dist < 1 and local_point.y <= self.minimum + Constants.epsilon:
            return Vector(0, -1, 0)
        else:
            return self.local_normal_at_wall(local_point)

    @abstractmethod
    def local_normal_at_wall(self, local_point: Point) -> Vector:
        pass
    
    # a helper function to reduce duplication
    # checks to see if the intersection at 't' is within a radius
    # from the y axis
    def check_cap(ray: Ray, t: float, radius: float) -> bool:
        x = ray.origin.x + t * ray.direction.x
        z = ray.origin.z + t * ray.direction.z

        return (x ** 2 + z ** 2) <= abs(radius)

    def intersect_caps(shape: 'RevolvedPlane', ray: Ray, xs: Iterable[Intersection]) -> None:
        # caps only matter if the shape is closed, and might possibly be
        # intersected by the ray
        if shape.closed is False or abs(ray.direction.y) < Constants.epsilon:
            return

        # check for an intersection with the lower end cap by intersectig
        # the ray with the plane at y=cyl.minimum
        t0 = (shape.minimum - ray.origin.y) / ray.direction.y

        # check for an intersection with the upper end cap by intersecting
        # the ray with the plane at y=cyl.maximum
        t1 = (shape.maximum - ray.origin.y) / ray.direction.y

        shape.local_intersect_caps(ray, xs, t0, t1)

    @abstractmethod
    def local_intersect_caps(self: 'RevolvedPlane', ray: Ray, xs: Iterable[Intersection], t0, t1) -> None:
        pass
        
    def find_intersections(self, ray, a, b, c) -> Iterable[Intersection]:
        disc = b ** 2 - 4 * a * c

        # ray does not intersect shape
        if disc < 0:
            return []

        t0 = (-b - math.sqrt(disc)) / (2 * a)
        t1 = (-b + math.sqrt(disc)) / (2 * a)

        # for truncated shapes
        xs = []

        y0 = ray.origin.y + t0 * ray.direction.y
        if self.minimum < y0 and y0 < self.maximum:
            xs.append(Intersection(t0, self))

        y1 = ray.origin.y + t1 * ray.direction.y
        if self.minimum < y1 and y1 < self.maximum:
            xs.append(Intersection(t1, self))

        return xs
