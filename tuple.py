import math

class Tuple:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w

    def __add__(self, other):
        return Tuple(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        return Tuple(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def scalar_multiply(self, multiplier):
        return Tuple(self.x * multiplier, self.y * multiplier, self.z * multiplier, self.w * multiplier)

    def scalar_divide(self, divisor):
        return Tuple(self.x / divisor, self.y / divisor, self.z / divisor, self.w / divisor)

    def __neg__(self):
        return self.scalar_multiply(-1)

    # TODO: should this be in Vector?
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w **2)

    # TODO: should this be in Vector?
    def normalize(self):
        # TODO: Can only normalize non-zero magnitude vectors
        magnitude = self.magnitude()
        return Tuple(self.x / magnitude, self.y / magnitude, self.z / magnitude, self.w / magnitude)

    # TODO: should this be in Vector?
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

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