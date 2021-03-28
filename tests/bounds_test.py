import math
import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from bounds import Bounds
from collections import namedtuple
from ray import Ray
from tuple import *
from transformations import Transformations

class TestBoundingBoxes(unittest.TestCase):
    # Scenario: Creating an empty bounding box
    def test_creating_empty_bounding_box(self):
        box = Bounds()
        self.assertEqual(box.min, Point(math.inf, math.inf, math.inf))
        self.assertEqual(box.max, Point(-math.inf, -math.inf, -math.inf))

    # Scenario: Creating a bounding box with volume
    def test_creating_bounding_box_with_volume(self):
        box = Bounds(Point(-1, -2, -3), Point(3, 2, 1))
        self.assertEqual(box.min, Point(-1, -2, -3))
        self.assertEqual(box.max, Point(3, 2, 1))

    # Scenario: Adding points to an empty bounding box
    def test_add_points_to_empty_bounding_box(self):
        box = Bounds()
        p1 = Point(-5, 2, 0)
        p2 = Point(7, 0, -3)
        box.add_point(p1)
        box.add_point(p2)
        self.assertEqual(box.min, Point(-5, 0, -3))
        self.assertEqual(box.max, Point(7, 2, 0))

    # Scenario: Adding one bounding box to another
    def test_add_bounding_box_to_another(self):
        box1 = Bounds(Point(-5, -2, 0), Point(7, 4, 4))
        box2 = Bounds(Point(8, -7, -2), Point(14, 2, 8))
        box1.add_box(box2)
        self.assertEqual(box1.min, Point(-5, -7, -2))
        self.assertEqual(box1.max, Point(14, 4, 8))

    # Scenario Outline: Checking to see if a box contains a given point
    def test_box_countains_point(self):
        box = Bounds(Point(5, -2, 0), Point(11, 4, 7))
        PointResult = namedtuple("PointResult", ["point", "result"])
        point_results = [
            PointResult(Point(5, -2, 0), True),
            PointResult(Point(11, 4, 7), True),
            PointResult(Point(8, 1, 3), True),
            PointResult(Point(3, 0, 3), False),
            PointResult(Point(8, -4, 3), False),
            PointResult(Point(8, 1, -1), False),
            PointResult(Point(13, 1, 3), False),
            PointResult(Point(8, 5, 3), False),
            PointResult(Point(8, 1, 8), False)
        ]
        for point_result in point_results:
            p = point_result.point
            self.assertEqual(box.box_contains_point(p), point_result.result)

    # Scenario Outline: Checking to see if a box contains a given box
    def test_box_contains_box(self):
        box = Bounds(Point(5, -2, 0), Point(11, 4, 7))
        BoundsResult = namedtuple("BoundsResult", ["min", "max", "result"])
        bounds_results = [
            BoundsResult(Point(5, -2, 0), Point(11, 4, 7), True),
            BoundsResult(Point(6, -1, 1), Point(10, 3, 6), True),
            BoundsResult(Point(4, -3, -1), Point(10, 3, 6), False),
            BoundsResult(Point(6, -1, 1), Point(12, 5, 8), False)
        ]
        for bounds_result in bounds_results:
            box2 = Bounds(bounds_result.min, bounds_result.max)
            self.assertEqual(box.box_contains_box(box2), bounds_result.result)

    # Scenario: Transforming a bounding box
    def test_tranforming_bounding_box(self):
        box = Bounds(Point(-1, -1, -1), Point(1, 1, 1))
        matrix = Transformations.rotation_x(math.pi / 4).dot(Transformations.rotation_y(math.pi / 4))
        box2 = box.transform(matrix)
        self.assertEqual(box2.min, Point(-1.4142, -1.7071, -1.7071))
        self.assertEqual(box2.max, Point(1.4142, 1.7071, 1.7071))

    # Scenario Outline: Intersecting a ray with a bounding box at the origin
    def test_intersect_ray_with_bounding_box_at_origin(self):
        box = Bounds(Point(-1, -1, -1), Point(1, 1, 1))
        RayResult = namedtuple("RayResult", ["origin", "direction", "result"])
        ray_results = [
            RayResult(Point(5, 0.5, 0), Vector(-1, 0, 0), True ),
            RayResult(Point(-5, 0.5, 0), Vector(1, 0, 0), True ),
            RayResult(Point(0.5, 5, 0), Vector(0, -1, 0), True ),
            RayResult(Point(0.5, -5, 0), Vector(0, 1, 0), True ),
            RayResult(Point(0.5, 0, 5), Vector(0, 0, -1), True ),
            RayResult(Point(0.5, 0, -5), Vector(0, 0, 1), True ),
            RayResult(Point(0, 0.5, 0), Vector(0, 0, 1), True ),
            RayResult(Point(-2, 0, 0), Vector(2, 4, 6), False),
            RayResult(Point(0, -2, 0), Vector(6, 2, 4), False),
            RayResult(Point(0, 0, -2), Vector(4, 6, 2), False),
            RayResult(Point(2, 0, 2), Vector(0, 0, -1), False),
            RayResult(Point(0, 2, 2), Vector(0, -1, 0), False),
            RayResult(Point(2, 2, 0), Vector(-1, 0, 0), False)
        ]
        for ray_result in ray_results:
            direction = Vector.normalize(ray_result.direction)
            r = Ray(ray_result.origin, direction)
            self.assertEqual(box.intersects(r), ray_result.result)

    # Scenario Outline: Intersecting a ray with a non-cubic bounding box
    def test_intersect_ray_with_noncubic_bouding_box(self):
        box = Bounds(Point(5, -2, 0), Point(11, 4, 7))
        RayResult = namedtuple("RayResult", ["origin", "direction", "result"])
        ray_results = [
            RayResult(Point(15, 1, 2), Vector(-1, 0, 0), True),
            RayResult(Point(-5, -1, 4), Vector(1, 0, 0) , True),
            RayResult(Point(7, 6, 5), Vector(0, -1, 0), True),
            RayResult(Point(9, -5, 6), Vector(0, 1, 0) , True),
            RayResult(Point(8, 2, 12), Vector(0, 0, -1), True),
            RayResult(Point(6, 0, -5), Vector(0, 0, 1) , True),
            RayResult(Point(8, 1, 3.5), Vector(0, 0, 1) , True),
            RayResult(Point(9, -1, -8), Vector(2, 4, 6) , False),
            RayResult(Point(8, 3, -4), Vector(6, 2, 4) , False),
            RayResult(Point(9, -1, -2), Vector(4, 6, 2) , False),
            RayResult(Point(4, 0, 9), Vector(0, 0, -1), False),
            RayResult(Point(8, 6, -1), Vector(0, -1, 0), False),
            RayResult(Point(12, 5, 4), Vector(-1, 0, 0), False)
        ]
        for ray_result in ray_results:
            direction = Vector.normalize(ray_result.direction)
            r = Ray(ray_result.origin, direction)
            self.assertEqual(box.intersects(r), ray_result.result)

if __name__ == '__main__':
    unittest.main()
    