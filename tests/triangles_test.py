import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from ray import Ray
from triangle import Triangle
from tuple import *

class TestTriangles(unittest.TestCase):
    # Scenario: Constructing a triangle
    def test_constructing_Triangle(self):
        p1 = Point(0, 1, 0)
        p2 = Point(-1, 0, 0)
        p3 = Point(1, 0, 0)
        t = Triangle(p1, p2, p3)
        self.assertEqual(t.p1, p1)
        self.assertEqual(t.p2, p2)
        self.assertEqual(t.p3, p3)
        self.assertEqual(t.e1, Vector(-1, -1, 0))
        self.assertEqual(t.e2, Vector(1, -1, 0))
        self.assertEqual(t.normal, Vector(0, 0, -1))

    # Scenario: Finding the normal on a triangle
    def test_normal_Triangle(self):
        t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        n1 = t.local_normal_at(Point(0, 0.5, 0))
        n2 = t.local_normal_at(Point(-0.5, 0.75, 0))
        n3 = t.local_normal_at(Point(0.5, 0.25, 0))
        self.assertEqual(n1, t.normal)
        self.assertEqual(n2, t.normal)
        self.assertEqual(n3, t.normal)

    # Scenario: Intersecting a ray parallel to the triangle
    def test_intersect_ray_parallel_Triangle(self):
        t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        r = Ray(Point(0, -1, -2), Vector(0, 1, 0))
        xs = t.local_intersect(r)
        self.assertEqual(len(xs), 0)

    # Scenario: A ray misses the p1-p3 edge
    def test_ray_misses_p1_p3_edge(self):
        t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        r = Ray(Point(1, 1, -2), Vector(0, 0, 1))
        xs = t.local_intersect(r)
        self.assertEqual(len(xs), 0)

    # Scenario: A ray misses the p1-p2 edge
    def test_ray_misses_p1_p2_edge(self):
        t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        r = Ray(Point(-1, 1, -2), Vector(0, 0, 1))
        xs = t.local_intersect(r)
        self.assertEqual(len(xs), 0)

    # Scenario: A ray misses the p2-p3 edge
    def test_ray_misses_p2_p3_edge(self):
        t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        r = Ray(Point(0, -1, -2), Vector(0, 0, 1))
        xs = t.local_intersect(r)
        self.assertEqual(len(xs), 0)

    # Scenario: A ray strikes a triangle
    def test_ray_strikes_Triangle(self):
        t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        r = Ray(Point(0, 0.5, -2), Vector(0, 0, 1))
        xs = t.local_intersect(r)
        self.assertEqual(len(xs), 1)
        self.assertEqual(xs[0].t, 2)

    # Scenario: A triangle has a bounding box
    def test_triangle_bounding_box(self):
        p1 = Point(-3, 7, 2)
        p2 = Point(6, 2, -4)
        p3 = Point(2, -1, -1)
        shape = Triangle(p1, p2, p3)
        box = shape.bounds_of()
        self.assertEqual(box.min, Point(-3, -1, -4))
        self.assertEqual(box.max, Point(6, 7, 2))

if __name__ == '__main__':
    unittest.main()
    