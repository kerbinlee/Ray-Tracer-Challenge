import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from collections import namedtuple
from csg import CSG
from cube import Cube
from group import Group
from intersection import Intersection
from ray import Ray
from shape import TestShape
from sphere import Sphere
from transformations import Transformations
from tuple import *

class TestCSG(unittest.TestCase):
    # Scenario: CSG is created with an operation and two shapes
    def test_csg_create(self):
        s1 = Sphere()
        s2 = Sphere()
        c = CSG("union", s1, s2)
        self.assertEqual(c.operation, "union")
        self.assertEqual(c.left, s1)
        self.assertEqual(c.right, s2)
        self.assertEqual(s1.parent, c)
        self.assertEqual(s2.parent, c)

    # Scenario Outline: Evaluating the rule for a CSG operation
    def test_csg_operation_rule(self):
        OperationResult = namedtuple("OperationResult", ["op", "lhit", "inl", "inr", "result"])
        operation_results = [
            OperationResult("union", True, True, True, False),
            OperationResult("union", True, True, False, True),
            OperationResult("union", True, False, True, False),
            OperationResult("union", True, False, False, True),
            OperationResult("union", False, True, True, False),
            OperationResult("union", False, True, False, False),
            OperationResult("union", False, False, True, True),
            OperationResult("union", False, False, False, True),
            OperationResult("intersection", True, True, True, True),
            OperationResult("intersection", True, True, False, False),
            OperationResult("intersection", True, False, True, True),
            OperationResult("intersection", True, False, False, False),
            OperationResult("intersection", False, True, True, True),
            OperationResult("intersection", False, True, False, True),
            OperationResult("intersection", False, False, True, False),
            OperationResult("intersection", False, False, False, False),
            OperationResult("difference", True, True, True, False),
            OperationResult("difference", True, True, False, True),
            OperationResult("difference", True, False, True, False),
            OperationResult("difference", True, False, False, True),
            OperationResult("difference", False, True, True, True),
            OperationResult("difference", False, True, False, True),
            OperationResult("difference", False, False, True, False),
            OperationResult("difference", False, False, False, False)
        ]
        for operation_result in operation_results:
            result = CSG.intersection_allowed(operation_result.op, operation_result.lhit, operation_result.inl, operation_result.inr)
            self.assertEqual(result, operation_result.result)

    # Scenario Outline: Filtering a list of intersections
    def test_filtering_list_intersections(self):
        s1 = Sphere()
        s2 = Cube()
        Operation = namedtuple("Operation", ["operation", "x0", "x1"])
        operatios = [
            Operation("union", 0, 3),
            Operation("intersection", 1, 2),
            Operation("difference", 0, 1)
        ]
        for operation in operatios:
            c = CSG(operation.operation, s1, s2)
            xs = Intersection.intersections(Intersection(1, s1), Intersection(2, s2), Intersection(3, s1), Intersection(4, s2))
            result = c.filter_intersections(xs)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0], xs[operation.x0])
            self.assertEqual(result[1], xs[operation.x1])

    # Scenario: A ray misses a CSG object
    def test_ray_misses_csg_object(self):
        c = CSG("union", Sphere(), Sphere())
        r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
        xs = c.local_intersect(r)
        self.assertEqual(len(xs), 0)

    # Scenario: A ray hits a CSG object
    def test_ray_hits_csg_object(self):
        s1 = Sphere()
        s2 = Sphere()
        s2.transform = Transformations.translation(0, 0, 0.5)
        c = CSG("union", s1, s2)
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = c.local_intersect(r)
        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, 4)
        self.assertEqual(xs[0].object, s1)
        self.assertEqual(xs[1].t, 6.5)
        self.assertEqual(xs[1].object, s2)

    # Scenario: A CSG shape has a bounding box that contains its children
    def test_csg_bounding_box(self):
        left = Sphere()
        right = Sphere()
        right.transform = Transformations.translation(2, 3, 4)
        shape = CSG("difference", left, right)
        box = shape.bounds_of()
        self.assertEqual(box.min, Point(-1, -1, -1))
        self.assertEqual(box.max, Point(3, 4, 5))

    # Scenario: Intersecting ray+csg doesn't test children if box is missed
    def test_intersect_ray_csg_test_no_children(self):
        left = TestShape()
        right = TestShape()
        shape = CSG("difference", left, right)
        r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
        xs = shape.intersect(r)
        self.assertIsNone(left.saved_ray)
        self.assertIsNone(right.saved_ray)

    # Scenario: Intersecting ray+csg tests children if box is hit
    def test_intersect_ray_csg_test_children(self):
        left = TestShape()
        right = TestShape()
        shape = CSG("difference", left, right)
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = shape.intersect(r)
        self.assertIsNotNone(left.saved_ray)
        self.assertIsNotNone(right.saved_ray)

    # Scenario: Subdividing a CSG shape subdivides its children
    def test_subdivide_csg_subdivide_children(self):
        s1 = Sphere()
        s1.transform = Transformations.translation(-1.5, 0, 0)
        s2 = Sphere()
        s2.transform = Transformations.translation(1.5, 0, 0)
        left = Group()
        left.add_child(s1)
        left.add_child(s2)
        s3 = Sphere()
        s3.transform = Transformations.translation(0, 0, -1.5)
        s4 = Sphere()
        s4.transform = Transformations.translation(0, 0, 1.5)
        right = Group()
        right.add_child(s3)
        right.add_child(s4)
        shape = CSG("difference", left, right)
        shape.divide(1)
        self.assertIsInstance(left.members[0], Group)
        self.assertEqual(left.members[0].members, [s1])
        self.assertIsInstance(left.members[1], Group)
        self.assertEqual(left.members[1].members, [s2])
        self.assertIsInstance(right.members[0], Group)
        self.assertEqual(right.members[0].members, [s3])
        self.assertIsInstance(right.members[1], Group)
        self.assertEqual(right.members[1].members, [s4])

if __name__ == '__main__':
    unittest.main()
