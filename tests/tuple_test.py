import os, sys
import unittest
import math
sys.path.append(os.path.abspath('..'))
from tuple import *

class TestTuple(unittest.TestCase):
    def test_point(self):
        a = Tuple(4.3, -4.2, 3.1, 1.0)
        self.assertEqual(a, Point(4.3, -4.2, 3.1))

    def test_vector(self):
        a = Tuple(4.3, -4.2, 3.1, 0.0)
        self.assertEqual(a, Vector(4.3, -4.2, 3.1))

    def test_point_tuple(self):
        p = Point(4, -4, 3)
        self.assertEqual(p, Tuple(4, -4, 3, 1))

    def test_vector_tuple(self):
        v = Vector(4, -4, 3)
        self.assertEqual(v, Tuple(4, -4, 3, 0))

    def test_add_tuples(self):
        a1 = Tuple(3, -2, 5, 1)
        a2 = Tuple(-2, 3, 1, 0)
        self.assertEqual(a1 + a2, Tuple(1, 1, 6, 1))

    def test_subtract_points(self):
        p1 = Point(3, 2, 1)
        p2 = Point(5, 6, 7)
        self.assertEqual(p1 - p2, Vector(-2, -4, -6))

    def test_subtract_vector_from_point(self):
        p = Point(3, 2, 1)
        v = Vector(5, 6, 7)
        self.assertEqual(p - v, Point(-2, -4, -6))

    def test_subtract_vectors(self):
        v1 = Vector(3, 2, 1)
        v2 = Vector(5, 6, 7)
        self.assertEqual(v1 - v2, Vector(-2, -4, -6))

    def test_negate_tuple(self):
        a = Tuple(1, -2, 3, -4)
        self.assertEqual(-a, Tuple(-1, 2, -3, 4))

    def test_scalar_multiplication(self):
        a = Tuple(1, -2, 3, -4)
        self.assertEqual(a * 3.5, Tuple(3.5, -7, 10.5, -14))

    def test_scalar_multiplication_fractions(self):
        a = Tuple(1, -2, 3, -4)
        self.assertEqual(a * 0.5, Tuple(0.5, -1, 1.5, -2))

    def test_scalar_division(self):
        a = Tuple(1, -2, 3, -4)
        self.assertEqual(a / 2, Tuple(0.5, -1, 1.5, -2))

    def test_magnitude_x(self):
        v = Vector(1, 0, 0)
        self.assertEqual(v.magnitude(), 1)

    def test_magnitude_y(self):
        v = Vector(0, 1, 0)
        self.assertEqual(v.magnitude(), 1)

    def test_magnitude_z(self):
        v = Vector(0, 0, 1)
        self.assertEqual(v.magnitude(), 1)

    def test_magnitude_1(self):
        v = Vector(1, 2, 3)
        self.assertEqual(v.magnitude(), math.sqrt(14))

    def test_magnitude_2(self):
        v = Vector(-1, -2, -3)
        self.assertEqual(v.magnitude(), math.sqrt(14))
        
    def test_normalize_1(self):
        v = Vector(4, 0, 0)
        self.assertEqual(v.normalize(), Vector(1, 0, 0))

    def test_normalize_2(self):
        v = Vector(1, 2, 3)
        self.assertEqual(v.normalize(), Vector(1 / math.sqrt(14), 2 / math.sqrt(14), 3 / math.sqrt(14)))

    def test_magniture_normalized(self):
        v = Vector(1, 2, 3)
        self.assertEqual(v.normalize().magnitude(), 1)

    def test_dot_product(self):
        a = Vector(1, 2, 3)
        b = Vector(2, 3, 4)
        self.assertEqual(a.dot(b), 20)

    def test_cross_product(self):
        a = Vector(1, 2, 3)
        b = Vector(2, 3, 4)
        self.assertEqual(a.cross(b), Vector(-1, 2, -1))
        self.assertEqual(b.cross(a), Vector(1, -2, 1))
        
if __name__ == '__main__':
    unittest.main()