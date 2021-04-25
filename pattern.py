from matrix import Matrix
from shape import Shape
from color import Color
from tuple import Point

from abc import ABC, abstractmethod
import math
import numpy as np

class Pattern(ABC):
    def __init__(self, color_a: Color, color_b: Color):
        self.a: Color = color_a
        self.b: Color = color_b
        self.transform: np.ndarray = np.identity(4)
    
    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and np.array_equal(self.transform, other.transform)

    def pattern_at_shape(self, shape: Shape, world_point: Point) -> Color:
        object_point = shape.world_to_object(world_point)
        pattern_point = Matrix.multiply_tuple(Matrix.inverse(self.transform), object_point)
        return self.pattern_at(pattern_point)

    @abstractmethod
    def pattern_at(self, pattern_point: Point) -> Color:
        pass

    def test_pattern() -> 'Pattern':
        return TestPattern()

class TestPattern(Pattern):
    def __init__(self):
        super().__init__(Color(0, 0, 0), Color(0, 0, 0))

    def pattern_at(self, pattern_point: Point) -> Color:
        super().pattern_at(pattern_point)
        return Color(pattern_point.x, pattern_point.y, pattern_point.z)
    
class Stripe(Pattern):
    def stripe_at(pattern: 'Pattern', point: Point) -> Color:
        if math.floor(point.x) % 2 is 0:
            return pattern.a
        else:
            return pattern.b

    def pattern_at(self, pattern_point: Point) -> Color:
        super().pattern_at(pattern_point)
        return Stripe.stripe_at(self, pattern_point)

class Gradient(Pattern):
    def pattern_at(self, pattern_point: Point) -> Color:
        super().pattern_at(pattern_point)
        distance = self.b - self.a
        fraction = pattern_point.x - math.floor(pattern_point.x)
        return self.a + distance * fraction

class Ring(Pattern):
    def pattern_at(self, pattern_point: Point) -> Color:
        super().pattern_at(pattern_point)
        if math.floor(math.sqrt(pattern_point.x ** 2 + pattern_point.z ** 2)) % 2 is 0:
            return self.a
        else:
            return self.b
    
class Checkers(Pattern):
    def pattern_at(self, pattern_point: Point) -> Color:
        super().pattern_at(pattern_point)
        if (math.floor(pattern_point.x) + math.floor(pattern_point.y) + math.floor(pattern_point.z)) % 2 is 0:
            return self.a
        else:
            return self.b
            