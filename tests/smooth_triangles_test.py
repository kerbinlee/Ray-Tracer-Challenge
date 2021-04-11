import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from computations import Computations
from intersection import Intersection
from ray import Ray
from smooth_triangle import SmoothTriangle
from tuple import *

class TestSmoothTriangles(unittest.TestCase):
    # Background:
    def setUp(self):
        self.p1 = Point(0, 1, 0)
        self.p2 = Point(-1, 0, 0)
        self.p3 = Point(1, 0, 0)
        self.n1 = Vector(0, 1, 0)
        self.n2 = Vector(-1, 0, 0)
        self.n3 = Vector(1, 0, 0)
        self.tri = SmoothTriangle(self.p1, self.p2, self.p3, self.n1, self.n2, self.n3)

    # Scenario: Constructing a smooth triangle
    def test_constructing_smooth_triangle(self):
        self.assertEqual(self.tri.p1, self.p1)
        self.assertEqual(self.tri.p2, self.p2)
        self.assertEqual(self.tri.p3, self.p3)
        self.assertEqual(self.tri.n1, self.n1)
        self.assertEqual(self.tri.n2, self.n2)
        self.assertEqual(self.tri.n3, self.n3)

    # Scenario: An intersection with a smooth triangle stores u/v
    def test_intersection_with_smooth_triangle_u_v(self):
        r = Ray(Point(-0.2, 0.3, -2), Vector(0, 0, 1))
        xs = self.tri.local_intersect(r)
        self.assertAlmostEqual(xs[0].u, 0.45, delta = Constants.epsilon)
        self.assertAlmostEqual(xs[0].v, 0.25, delta = Constants.epsilon)

    # Scenario: A smooth triangle uses u/v to interpolate the normal
    def test_smooth_triangle_interpolate_normal(self):
        i = Intersection(1, self.tri, 0.45, 0.25)
        n = self.tri.normal_at(Point(0, 0, 0), i)
        self.assertEqual(n, Vector(-0.5547, 0.83205, 0))

    # Scenario: Preparing the normal on a smooth triangle
    def test_preparing_normal_smooth_triangle(self):
        i = Intersection(1, self.tri, 0.45, 0.25)
        r = Ray(Point(-0.2, 0.3, -2), Vector(0, 0, 1))
        xs = Intersection.intersections(i)
        comps = Computations.prepare_computations(i, r, xs)
        self.assertEqual(comps.normalv, Vector(-0.5547, 0.83205, 0))

if __name__ == '__main__':
    unittest.main()
