from bounds import Bounds
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
        bounds = self.bounds_of()
        if bounds.intersects(ray):
            xs = []
            for member in self.members:
                xs.extend(member.intersect(ray))

            return sorted(xs, key = lambda intersection: intersection.t)
        else:
            return []

    def local_normal_at(self, local_point: Point = None) -> Vector:
        raise Exception("Group.local_normal_at should not be called. Group is abstract, use concrete shapes' local_normal_at")

    def add_child(self, shape: Shape) -> None:
        shape.parent = self
        self.members.append(shape)

    def bounds_of(self) -> Bounds:
        box = Bounds()
        for child in self.members:
            cbox = child.parent_space_bounds_of()
            box.add_box(cbox)

        return box
