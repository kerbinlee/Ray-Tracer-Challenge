import numpy as np

from abc import ABC, abstractmethod
from bounds import Bounds
from intersection import Intersection
from material import Material
from matrix import Matrix
from ray import Ray
from tuple import *
from typing import Iterable

class Shape(ABC):
    def __init__(self):
        self.material: Material = Material()
        self.transform: np.ndarray = np.identity(4)
        self.parent: 'Shape' = None

    @abstractmethod
    def __eq__(self, other):
        return np.array_equal(self.transform, other.transform) and self.material == other.material

    def test_shape() -> 'TestShape':
        return TestShape()

    def intersect(self, ray: Ray) -> Iterable[Intersection]:
        local_ray = Ray.transform(ray, Matrix.inverse(self.transform))
        return self.local_intersect(local_ray)

    @abstractmethod
    def local_intersect(self, ray: Ray) -> Iterable[Intersection]:
        pass

    def normal_at(self, point: Point, intersection: Intersection = None) -> Tuple:
        local_point = self.world_to_object(point)
        local_normal = self.local_normal_at(local_point, intersection)
        return self.normal_to_world(local_normal)

    @abstractmethod
    def local_normal_at(self, local_point: Point, intersection: Intersection) -> Vector:
        pass

    def world_to_object(self, point: Point) -> Point:
        if self.parent is not None:
            point = self.parent.world_to_object(point)
        
        return Matrix.multiply_tuple(Matrix.inverse(self.transform), point)

    def normal_to_world(self, normal: Vector) -> Vector:
        normal = Matrix.multiply_tuple(Matrix.inverse(self.transform).transpose(), normal)
        normal.w = 0
        normal = Vector.normalize(normal)

        if self.parent is not None:
            normal = self.parent.normal_to_world(normal)

        return normal

    # calculate untransformed bounds of a given shape
    @abstractmethod
    def bounds_of(self) -> Bounds:
        pass

    def parent_space_bounds_of(self)-> Bounds:
        return self.bounds_of().transform(self.transform)

class TestShape(Shape):
    def __init__(self):
        super().__init__()
        self.saved_ray = None

    def __eq__(self, other):
        return super().__eq__(other)

    def local_intersect(self, ray: Ray) -> Iterable[Intersection]:
        self.saved_ray = ray
        return []

    def local_normal_at(self, local_point: Point) -> Vector:
        super().local_normal_at(local_point)
        return Vector(local_point.x, local_point.y, local_point.z)

    def bounds_of(self) -> Bounds:
        min = Point(-1, -1, -1)
        max = Point(1, 1, 1)
        return Bounds(min, max)
        