
from bounds import Bounds
from group import Group
from intersection import Intersection
from ray import Ray
from shape import Shape
from tuple import *
from typing import List


class CSG(Shape):
    def __init__(self, operation: str, left: Shape, right: Shape):
        super().__init__()
        self.operation: str = operation
        self.left: Shape = left
        self.left.parent = self
        self.right: Shape = right
        self.right.parent = self

    def __eq__(self, other):
        return super().__eq__(other) and self.operation == other.operation and self.left == other.left and self.right == other.right

    def intersection_allowed(op: str, lhit: bool, inl: bool, inr: bool) -> bool:
        if op == "union":
            return (lhit and not inr) or (not lhit and not inl)
        elif op == "intersection":
            return (lhit and inr) or (not lhit and inl)
        elif op == "difference":
            return (lhit and not inr) or (not lhit and inl)
        return False

    def filter_intersections(csg: 'CSG', xs: List[Intersection]) -> List[Intersection]:
        # begin outside of both children
        inl = False
        inr = False

        # prepare a list to receive the filtered intersections
        result = []

        for intersection in xs:
            # if i.object is part of the "left" child, then lhit is true
            lhit = CSG.includes(csg.left, intersection.object)

            if CSG.intersection_allowed(csg.operation, lhit, inl, inr):
                result.append(intersection)

            # depending on which object was hit, toggle either inl or inr
            if lhit:
                inl = not inl
            else:
                inr = not inr

        return result

    def includes(a: Shape, b: Shape) -> bool:
        if isinstance(a, Group):
            for child in a.members:
                if CSG.includes(child, b):
                    return True
            return False
        if isinstance(a, CSG):
            return CSG.includes(a.left, b) or CSG.includes(a.right, b)
        if isinstance(a, Shape):
            return a == b

    def local_intersect(self, ray: Ray) -> List[Intersection]:
        bounds = self.bounds_of()
        if bounds.intersects(ray):
            leftxs = self.left.intersect(ray)
            rightxs = self.right.intersect(ray)

            xs = list(leftxs + rightxs)
            xs.sort(key = lambda intersection: intersection.t)

            return CSG.filter_intersections(self, xs)
        else:
            return []

    def local_normal_at(self, local_point: Point, intersection: Intersection) -> Vector:
        pass

    def bounds_of(self) -> Bounds:
        box = Bounds()

        left_cbox = self.left.parent_space_bounds_of()
        right_cbox = self.right.parent_space_bounds_of()

        box.add_box(left_cbox)
        box.add_box(right_cbox)

        return box

    def divide(self, threshold: int) -> None:
        self.left.divide(threshold)
        self.right.divide(threshold)
