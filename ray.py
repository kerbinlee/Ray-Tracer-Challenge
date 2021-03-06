from tuple import *
from matrix import Matrix

class Ray:
    def __init__(self, origin: Point, direction: Vector):
        self.origin: Point = origin
        self.direction: Vector = direction

    def position(ray, distance):
        return ray.origin + ray.direction * distance

    def transform(ray, matrix):
        return Ray(Matrix.multiply_tuple(matrix, ray.origin), Matrix.multiply_tuple(matrix, ray.direction))
