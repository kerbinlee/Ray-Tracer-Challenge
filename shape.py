import numpy as np

from abc import ABC, abstractmethod
from intersection import Intersection
from material import Material
from matrix import Matrix
from ray import Ray
from tuple import *
from typing import Iterable

class Shape(ABC):
    def __init__(self):
        self.material = Material()
        self.transform = np.identity(4)

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

    def normal_at(self, point: Point) -> Tuple:
        local_point = Matrix.multiply_tuple(Matrix.inverse(self.transform), point)
        local_normal = self.local_normal_at(local_point)
        world_normal = Matrix.multiply_tuple(Matrix.inverse(self.transform).transpose(), local_normal)
        world_normal.w = 0
        return Vector.normalize(world_normal)

    @abstractmethod
    def local_normal_at(self, local_point: Point) -> Vector:
        pass

class TestShape(Shape):
    saved_ray = None
    def __init__(self):
        super().__init__()

    def __eq__(self, other):
        return super().__eq__(other)

    def local_intersect(self, ray: Ray) -> Iterable[Intersection]:
        self.saved_ray = ray

    def local_normal_at(self, local_point: Point) -> Vector:
        super().local_normal_at(local_point)
        return Vector(local_point.x, local_point.y, local_point.z)
        