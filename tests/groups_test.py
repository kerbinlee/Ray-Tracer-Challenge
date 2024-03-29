import numpy as np
import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from cylinder import Cylinder
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

    # Scenario: A group has a bounding box that contains its children
    def test_group_bounding_box_contains_children(self):
        s = Sphere()
        s.transform = Transformations.translation(2, 5, -3).dot(Transformations.scaling(2, 2, 2))
        c = Cylinder()
        c.minimum = -2
        c.maximum = 2
        c.transform = Transformations.translation(-4, -1, 4).dot(Transformations.scaling(0.5, 1, 0.5))
        shape = Group()
        shape.add_child(s)
        shape.add_child(c)
        box = shape.bounds_of()
        self.assertEqual(box.min, Point(-4.5, -3, -5))
        self.assertEqual(box.max, Point(4, 7, 4.5))

    # Scenario: Intersecting ray+group doesn't test children if box is missed
    def test_group_missed_boudning_box(self):
        child = Shape.test_shape()
        shape = Group()
        shape.add_child(child)
        r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
        xs = shape.intersect(r)
        self.assertIsNone(child.saved_ray)

    # Scenario: Intersecting ray+group tests children if box is hit
    def test_group_hit_bounding_box(self):
        child = Shape.test_shape()
        shape = Group()
        shape.add_child(child)
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = shape.intersect(r)
        self.assertIsNotNone(child.saved_ray)

    # Scenario: Partitioning a group's children
    def test_partitioning_group_children(self):
        s1 = Sphere()
        s1.transform = Transformations.translation(-2, 0, 0)
        s2 = Sphere()
        s2.transform = Transformations.translation(2, 0, 0)
        s3 = Sphere()
        g = Group()
        g.add_child(s1)
        g.add_child(s2)
        g.add_child(s3)
        (left, right) = g.partition_children()
        self.assertEqual(g.members, [s3])
        self.assertEqual(left, [s1])
        self.assertEqual(right, [s2])

    # Scenario: Creating a sub-group from a list of children
    def test_create_subgroup_from_children(self):
        s1 = Sphere()
        s2 = Sphere()
        g = Group()
        g.make_subgroup([s1, s2])
        self.assertEqual(len(g.members), 1)
        self.assertEqual(g.members[0].members, [s1, s2])

    # Scenario: Subdividing a group partitions its children
    def test_group_partitions_children(self):
        s1 = Sphere()
        s1.transform = Transformations.translation(-2, -2, 0)
        s2 = Sphere()
        s2.transform = Transformations.translation(-2, 2, 0)
        s3 = Sphere()
        s3.transform = Transformations.scaling(4, 4, 4)
        g = Group()
        g.add_child(s1)
        g.add_child(s2)
        g.add_child(s3)
        g.divide(1)
        self.assertEqual(g.members[0], s3)
        subgroup = g.members[1]
        self.assertIsInstance(subgroup, Group)
        self.assertEqual(len(subgroup.members), 2)
        self.assertEqual(subgroup.members[0].members, [s1])
        self.assertEqual(subgroup.members[1].members, [s2])

    # Scenario: Subdividing a group with too few children
    def test_subdividing_group_too_few_children(self):
        s1 = Sphere()
        s1.transform = Transformations.translation(-2, 0, 0)
        s2 = Sphere()
        s2.transform = Transformations.translation(2, 1, 0)
        s3 = Sphere()
        s3.transform = Transformations.translation(2, -1, 0)
        subgroup = Group()
        subgroup.add_child(s1)
        subgroup.add_child(s2)
        subgroup.add_child(s3)
        s4 = Sphere()
        g = Group()
        g.add_child(subgroup)
        g.add_child(s4)
        g.divide(3)
        self.assertEqual(g.members[0], subgroup)
        self.assertEqual(g.members[1], s4)
        self.assertEqual(len(subgroup.members), 2)
        self.assertEqual(subgroup.members[0].members, [s1])
        self.assertEqual(subgroup.members[1].members, [s2, s3])

if __name__ == '__main__':
    unittest.main()
    