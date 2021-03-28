import math
import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from plane import Plane
from ray import Ray
from tuple import *

class TestPlanes(unittest.TestCase):
    # Scenario: The normal of a plane is constant everywhere
    def test_normal_plane_constant(self):
        p = Plane()
        n1 = p.normal_at(Point(0, 0, 0))
        n2 = p.normal_at(Point(10, 0, -10))
        n3 = p.normal_at(Point(-5, 0, 150))
        self.assertEqual(n1, Vector(0, 1, 0))
        self.assertEqual(n2, Vector(0, 1, 0))
        self.assertEqual(n3, Vector(0, 1, 0))

    # Scenario: Intersect with a ray parallel to the plane
    def test_intersect_ray_parallel(self):
        p = Plane()
        r = Ray(Point(0, 10, 0), Vector(0, 0, 1))
        xs = p.intersect(r)
        self.assertEqual(xs, [])

    # Scenario: Intersect with a coplanar ray
    def test_intersect_coplanar_ray(self):
        p = Plane()
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        xs = p.intersect(r)
        self.assertEqual(xs, [])

    # Scenario: A ray intersecting a plane from above
    def test_intersect_above(self):
        p = Plane()
        r = Ray(Point(0, 1, 0), Vector(0, -1, 0))
        xs = p.intersect(r)
        self.assertEqual(len(xs), 1)
        self.assertEqual(xs[0].t, 1)
        self.assertEqual(xs[0].object, p)

    # Scenario: A ray intersecting a plane from below
    def test_intersect_below(self):
        p = Plane()
        r = Ray(Point(0, -1, 0), Vector(0, 1, 0))
        xs = p.intersect(r)
        self.assertEqual(len(xs), 1)
        self.assertEqual(xs[0].t, 1)
        self.assertEqual(xs[0].object, p)
    
    # Scenario: A plane has a bounding box
    def test_plane_bounding_box(self):
        shape = Plane()
        box = shape.bounds_of()
        self.assertEqual(box.min, Point(-math.inf, 0, -math.inf))
        self.assertEqual(box.max, Point(math.inf, 0, math.inf))
    
if __name__ == '__main__':
    unittest.main()
    