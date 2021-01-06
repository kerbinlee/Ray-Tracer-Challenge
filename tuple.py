import math
from constants import Constants

class Tuple:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __eq__(self, other):
        return abs(self.x - other.x) < Constants.epsilon and abs(self.y - other.y) < Constants.epsilon and abs(self.z - other.z) < Constants.epsilon and abs(self.w - other.w) < Constants.epsilon

    def __add__(self, other):
        return Tuple(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        return Tuple(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __mul__(self, other):
        return Tuple(self.x * other, self.y * other, self.z * other, self.w * other)

    def __truediv__(self, divisor):
        return Tuple(self.x / divisor, self.y / divisor, self.z / divisor, self.w / divisor)

    def __neg__(self):
        return self * -1

    # TODO: should this be in Vector?
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w **2)

    # TODO: should this be in Vector?
    def normalize(tuple: 'Tuple') -> 'Tuple':
        # TODO: Can only normalize non-zero magnitude vectors
        magnitude = tuple.magnitude()
        return Tuple(tuple.x / magnitude, tuple.y / magnitude, tuple.z / magnitude, tuple.w / magnitude)

    # TODO: should this be in Vector?
    def dot(a: 'Tuple', b: 'Tuple') -> float:
        return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w

    def __str__(self):
        return f"x={self.x} y={self.y} z={self.z}"

class Point(Tuple):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 1)

class Vector(Tuple):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 0)

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

    def reflect(in_vector: 'Vector', normal: 'Vector') -> 'Vector':
        return  in_vector - normal * 2 * Vector.dot(in_vector, normal)
