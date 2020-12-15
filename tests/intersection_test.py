import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from tuple import *
from intersection import Intersection
from sphere import Sphere

class TestIntersections(unittest.TestCase):
    # Scenario: An intersection encapsulates t and object
    def test_intersection_encapsulation(self):
        s = Sphere()
        i = Intersection(3.5, s)
        self.assertEqual(i.t, 3.5)
        self.assertEqual(i.object, s)
        
    # Scenario: Aggregating intersections
    def test_aggregate_intersections(self):
        s = Sphere()
        i1 = Intersection(1, s)
        i2 = Intersection(2, s)
        xs = Intersection.intersections(i1, i2)
        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, 1)
        self.assertEqual(xs[1].t, 2)

    # Scenario: The hit, when all intersections have positive t
    def test_hit_all_intersections_positive_t(self):
        s = Sphere()
        i1 = Intersection(1, s)
        i2 = Intersection(2, s)
        xs = Intersection.intersections(i2, i1)
        i = Intersection.hit(xs)
        self.assertEqual(i, i1)

    # Scenario: The hit, when some intersections have negative t
    def test_hit_some_intersections_negative_t(self):
        s = Sphere()
        i1 = Intersection(-1, s)
        i2 = Intersection(1, s)
        xs = Intersection.intersections(i2, i1)
        i = Intersection.hit(xs)
        self.assertEqual(i, i2)

    # Scenario: The hit, when all intersections have negative t
    def test_hit_all_intersections_negative_t(self):
        s = Sphere()
        i1 = Intersection(-2, s)
        i2 = Intersection(-1, s)
        xs = Intersection.intersections(i2, i1)
        i = Intersection.hit(xs)
        self.assertIsNone(i)

    # Scenario: The hit is always the lowest nonnegative intersection
    def test_hit_lowest_nonnegative_intersection(self):
        s = Sphere()
        i1 = Intersection(5, s)
        i2 = Intersection(7, s)
        i3 = Intersection(-3, s)
        i4 = Intersection(2, s)
        xs = Intersection.intersections(i1, i2, i3, i4)
        i = Intersection.hit(xs)
        self.assertEqual(i, i4)


if __name__ == '__main__':
    unittest.main()
