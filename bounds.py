import math

from matrix import Matrix
from tuple import Point
from typing import Tuple

class Bounds():
    def __init__(self, min: Point = None, max: Point = None):
        self.min: Point = Point(math.inf, math.inf, math.inf) if min is None else min
        self.max: Point = Point(-math.inf, -math.inf, -math.inf) if max is None else max

    def add_point(self, point: Point) -> None:
        if point.x < self.min.x:
            self.min.x = point.x
        if point.y < self.min.y:
            self.min.y = point.y
        if point.z < self.min.z:
            self.min.z = point.z

        if point.x > self.max.x:
            self.max.x = point.x 
        if point.y > self.max.y:
            self.max.y = point.y 
        if point.z > self.max.z:
            self.max.z = point.z 

    def add_box(self, box: 'Bounds') -> None:
        self.add_point(box.min)
        self.add_point(box.max)

    def box_contains_point(self, point: Point) -> bool:
        return self.min.x <= point.x <= self.max.x and self.min.y <= point.y <= self.max.y and self.min.z <= point.z <= self.max.z

    def box_contains_box(self, box: 'Bounds') -> bool:
        return self.box_contains_point(box.min) and self.box_contains_point(box.max)

    def transform(self, matrix) -> 'Bounds':
        p1 = self.min
        p2 = Point(self.min.x, self.min.y, self.max.z)
        p3 = Point(self.min.x, self.max.y, self.min.z)
        p4 = Point(self.min.x, self.max.y, self.max.z)
        p5 = Point(self.max.x, self.min.y, self.min.z)
        p6 = Point(self.max.x, self.min.y, self.max.z)
        p7 = Point(self.max.x, self.max.y, self.min.z)
        p8 = self.max

        new_bbox = Bounds()

        for p in [p1, p2, p3, p4, p5, p6, p7, p8]:
            new_bbox.add_point(Matrix.multiply_tuple(matrix, p))

        return new_bbox

    def intersects(self, ray) -> bool:
        from cube import Cube

        xtmin, xtmax = Cube.check_axis(ray.origin.x, ray.direction.x, self.min.x, self.max.x)
        ytmin, ytmax = Cube.check_axis(ray.origin.y, ray.direction.y, self.min.y, self.max.y)
        ztmin, ztmax = Cube.check_axis(ray.origin.z, ray.direction.z, self.min.z, self.max.z)

        tmin = max([xtmin, ytmin, ztmin])
        tmax = min([xtmax, ytmax, ztmax])

        if tmin > tmax:
            return False

        return True

    def split_bounds(box: 'Bounds') -> Tuple['Bounds', 'Bounds']:
        # figure out the box's largest dimension
        dx = box.max.x - box.min.x
        dy = box.max.y - box.min.y
        dz = box.max.z - box.min.z

        greatest = max(dx, dy, dz)

        # variables to help construct the points on
        # the dividing plane
        (x0, y0, z0) = (box.min.x, box.min.y, box.min.z)
        (x1, y1, z1) = (box.max.x, box.max.y, box.max.z)

        # adjust the points so that they lie on the
        # dividing plane
        if greatest == dx:
            x0 = x1 = x0 + dx / 2.0
        elif greatest == dy:
            y0 = y1 = y0 + dy / 2.0
        else:
            z0 = z1 = z0 + dz / 2.0

        mid_min = Point(x0, y0, z0)
        mid_max = Point(x1, y1, z1)

        # construct and return the two halves of
        # the bounding box
        left = Bounds(box.min,mid_max)
        right = Bounds(mid_min,box.max)

        return (left, right)
