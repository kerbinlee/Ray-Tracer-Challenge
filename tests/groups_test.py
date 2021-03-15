import numpy as np
import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from group import Group
from ray import Ray
from shape import Shape
from sphere import Sphere
from transformations import Transformations
from tuple import *

class TestGroups(unittest.TestCase):
    # Scenario: Creating a new group
    def test_create_new_group(self):
        g = Group()
        g.transform = np.identity(4)
        self.assertEqual(len(g.members), 0)

    # Scenario: Adding a child to a group
    def test_add_child_to_group(self):
        g = Group()
        s = Shape.test_shape()
        g.add_child(s)
        self.assertGreater(len(g.members), 0)
        self.assertTrue(s in g.members)
        self.assertEqual(s.parent, g)

    # Scenario: Intersecting a ray with an empty group
    def test_intersecting_ray_with_empty_group(self):
        g = Group()
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        xs = g.local_intersect(r)
        self.assertEqual(len(xs), 0)

    # Scenario: Intersecting a ray with a nonempty group
    def test_intersecting_ray_with_nonempty_group(self):
        g = Group()
        s1 = Sphere()
        s2 = Sphere()
        s2.transform = Transformations.translation(0, 0, -3)
        s3 = Sphere()
        s3.transform = Transformations.translation(5, 0, 0)
        g.add_child(s1)
        g.add_child(s2)
        g.add_child(s3)
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = g.local_intersect(r)
        self.assertEqual(len(xs), 4)
        self.assertEqual(xs[0].object, s2)
        self.assertEqual(xs[1].object, s2)
        self.assertEqual(xs[2].object, s1)
        self.assertEqual(xs[3].object, s1)

    # Scenario: Intersecting a transformed group
    def test_intersecting_transformed_group(self):
        g = Group()
        g.transform = Transformations.scaling(2, 2, 2)
        s = Sphere()
        s.transform = Transformations.translation(5, 0, 0)
        g.add_child(s)
        r = Ray(Point(10, 0, -10), Vector(0, 0, 1))
        xs = g.intersect(r)
        self.assertEqual(len(xs), 2)

    def test_local_normal_at_exception(self):
        g = Group()
        self.assertRaises(Exception, g.local_normal_at)

if __name__ == '__main__':
    unittest.main()
    