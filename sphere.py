from intersection import Intersection
from material import Material
from matrix import Matrix
from tuple import *
from ray import Ray

import numpy as np

import math

class Sphere:
    def __init__(self):
        self.origin: Point = Point(0, 0, 0)
        self.radius: float = 1
        self.transform: np.ndarray = np.identity(4)
        self.material: Material = Material()

    def __eq__(self, other):
        return self.origin == other.origin and self.radius == other.radius and np.array_equal(self.transform, other.transform) and self.material == other.material

    def intersect(sphere: 'Sphere', ray: Ray):
        ray2 = Ray.transform(ray, Matrix.inverse(sphere.transform))
        sphere_to_ray = ray2.origin - Point(0, 0, 0)
        a = Vector.dot(ray2.direction, ray2.direction)
        b = 2 * Vector.dot(ray2.direction, sphere_to_ray)
        c = Vector.dot(sphere_to_ray, sphere_to_ray) - 1
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return Intersection.intersections()

        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)

        return Intersection.intersections(Intersection(t1, sphere), Intersection(t2, sphere))

    def normal_at(sphere: 'Sphere', world_point: Point) -> Tuple:
        object_point = Matrix.multiply_tuple(Matrix.inverse(sphere.transform), world_point)
        object_normal = object_point - Point(0, 0, 0)
        world_normal = Matrix.multiply_tuple(Matrix.inverse(sphere.transform).transpose(), object_normal)
        world_normal.w = 0
        return Point.normalize(world_normal)
