from intersection import Intersection
from triangle import Triangle
from tuple import *

class SmoothTriangle(Triangle):
    def __init__(self, p1: Point, p2: Point, p3: Point, n1: Vector, n2: Vector, n3: Vector):
        super().__init__(p1, p2, p3)
        self.n1: Vector = n1
        self.n2: Vector = n2
        self.n3: Vector = n3
    
    def local_normal_at(self, local_point: Point = None, intersection: Intersection = None) -> Vector:
        return self.n2 * intersection.u + self.n3 * intersection.v + self.n1 * (1 -intersection.u - intersection.v)
        