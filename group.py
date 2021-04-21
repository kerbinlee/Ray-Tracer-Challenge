from bounds import Bounds
from intersection import Intersection
from ray import Ray
from shape import Shape
from tuple import *
from typing import Iterable, List

class Group(Shape):
    def __init__(self):
        super().__init__()
        self.members: List[Shape] = []
    
    def __eq__(self, other):
        return super().__eq__(other) and self.members == other.members

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

    def divide(self, threshold):
        if threshold <= len(self.members):
            (left, right) = self.partition_children()
            if len(left) != 0:
                self.make_subgroup([left])
                self.make_subgroup([right])

        for child in self.members:
            child.divide(threshold)

    def partition_children(self) -> Tuple:
        bounding_box = self.bounds_of()
        (left_box, right_box) = bounding_box.split_bounds()
        left_group_members = []
        right_group_members = []
        other_members = []
        for member in list(self.members):
            member_bounds = member.parent_space_bounds_of()
            if left_box.box_contains_box(member_bounds) and right_box.box_contains_box(member_bounds):
                other_members.append(member)
            elif left_box.box_contains_box(member_bounds):
                left_group_members.append(member)
            elif right_box.box_contains_box(member_bounds):
                right_group_members.append(member)
            else:
                other_members.append(member)
        self.members = other_members
        return (left_group_members, right_group_members)

    def make_subgroup(self, subgroup_members: List[Shape]) -> None:
        if len(subgroup_members) > 0:
            subgroup = Group()
            for member in subgroup_members:
                subgroup.add_child(member)

            self.add_child(subgroup)

    def divide(self, threshold: int) -> None:
        if threshold <= len(self.members):
            (left, right) = self.partition_children()
            if len(left) != 0:
                self.make_subgroup(left)
            if len(right) != 0:
                self.make_subgroup(right)

        for child in self.members:
            child.divide(threshold)
