import math

from matrix import Matrix
from tuple import Point

class Bounds():
    def __init__(self, min: Point = Point(math.inf, math.inf, math.inf), max: Point = Point(-math.inf, -math.inf, -math.inf)):
        self.min: Point = min
        self.max: Point = max

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
