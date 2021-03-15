from intersection import Intersection
from ray import Ray
from shape import Shape
from tuple import *
from typing import Iterable

class Group(Shape):
    def __init__(self):
        super().__init__()
        self.members: Iterable[Shape] = []
    
    def __eq__(self, other):
        return super().__eq__(other)

    def local_intersect(self, ray: Ray) -> Iterable[Intersection]:
        xs = []
        for member in self.members:
            xs.extend(member.intersect(ray))

        return sorted(xs, key = lambda intersection: intersection.t)

    def local_normal_at(self, local_point: Point = None) -> Vector:
        raise Exception("Group.local_normal_at should not be called. Group is abstract, use concrete shapes' local_normal_at")

    def add_child(self, shape: Shape) -> None:
        shape.parent = self
        self.members.append(shape)
