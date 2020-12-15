import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from transformations import Transformations
from tuple import *
from ray import Ray

class TestRay(unittest.TestCase):
    # Scenario: Creating and querying a ray
    def test_ray(self):
        origin = Point(1, 2, 3)
        direction = Vector(4, 5, 6)
        r = Ray(origin, direction)
        self.assertEqual(r.origin, origin)
        self.assertEqual(r.direction, direction)

    # Scenario: Computing a point from a distance
    def test_compute_point(self):
        r = Ray(Point(2, 3, 4), Vector(1, 0, 0))
        self.assertEqual(r.position(0), Point(2, 3, 4))
        self.assertEqual(r.position(1), Point(3, 3, 4))
        self.assertEqual(r.position(-1), Point(1, 3, 4))
        self.assertEqual(r.position(2.5), Point(4.5, 3, 4))

    # Scenario: Translating a ray
    def test_translate_ray(self):
        r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
        m = Transformations.translation(3, 4, 5)
        r2 = Ray.transform(r, m)
        self.assertEqual(r2.origin, Point(4, 6, 8))
        self.assertEqual(r2.direction, Vector(0, 1, 0))

    # Scenario: Scaling a ray
    def test_scale_ray(self):
        r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
        m = Transformations.scaling(2, 3, 4)
        r2 = Ray.transform(r, m)
        self.assertEqual(r2.origin, Point(2, 6, 12))
        self.assertEqual(r2.direction, Vector(0, 3, 0))
        

if __name__ == '__main__':
    unittest.main()
