import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from collections import namedtuple
from cone import Cone
from ray import Ray
from tuple import *

class TestCones(unittest.TestCase):
    # Scenario Outline: Intersecting a cone with a ray
    def test_intersect_cone_with_ray(self):
        shape = Cone()
        RayIntersection = namedtuple("RayIntersection", ["origin", "direction", "t0", "t1"])
        ray_intersections = [
            RayIntersection(Point(0, 0, -5), Vector(0, 0, 1), 5, 5),
            RayIntersection(Point(0, 0, -5), Vector(1, 1, 1), 8.66025, 8.66025),
            RayIntersection(Point(1, 1, -5), Vector(-0.5, -1, 1), 4.55006, 49.44994)
        ]
        for ray_intersection in ray_intersections:
            direction = Vector.normalize(ray_intersection.direction)
            r = Ray(ray_intersection.origin, direction)
            xs = shape.local_intersect(r)
            self.assertEqual(len(xs), 2)
            self.assertAlmostEqual(xs[0].t, ray_intersection.t0, delta = Constants.epsilon)
            self.assertAlmostEqual(xs[1].t, ray_intersection.t1, delta = Constants.epsilon)

    # Scenario: Intersecting a cone with a ray parallel to one of its halves
    def test_intersect_cone_with_ray_parallel_to_half(self):
        shape = Cone()
        direction = Vector.normalize(Vector(0, 1, 1))
        r = Ray(Point(0, 0, -1), direction)
        xs = shape.local_intersect(r)
        self.assertEqual(len(xs), 1)
        self.assertAlmostEqual(xs[0].t, 0.35355, delta = Constants.epsilon)

    # Scenario Outline: Intersecting a cone's end caps
    def test_intersect_cone_end_cap(self):
        shape = Cone()
        shape.minimum = -0.5
        shape.maximum = 0.5
        shape.closed = True
        RayIntersection = namedtuple("RayIntersection", ["origin", "direction", "count"])
        ray_intersections = [
            RayIntersection(Point(0, 0, -5), Vector(0, 1, 0), 0),
            RayIntersection(Point(0, 0, -0.25), Vector(0, 1, 1), 2),
            RayIntersection(Point(0, 0, -0.25), Vector(0, 1, 0), 4)
        ]
        for ray_intersection in ray_intersections:
            direction = Vector.normalize(ray_intersection.direction)
            r = Ray(ray_intersection.origin, direction)
            xs = shape.local_intersect(r)
            self.assertEqual(len(xs), ray_intersection.count)

    # Scenario Outline: Computing the normal vector on a cone
    def test_normal_vector_on_cone(self):
        shape = Cone()
        PointNormal = namedtuple("PointNormal", ["point", "normal"])
        point_normals = [
            PointNormal(Point(0, 0, 0), Vector(0, 0, 0)),
            PointNormal(Point(1, 1, 1), Vector(1, -math.sqrt(2), 1)),
            PointNormal(Point(-1, -1, 0), Vector(-1, 1, 0) )
        ]
        for point_normal in point_normals:
            n = shape.local_normal_at(point_normal.point)
            self.assertEqual(n, point_normal.normal)

    # Scenario: An unbounded cone has a bounding box
    def test_unbounded_cone_bounding_box(self):
        shape = Cone()
        box = shape.bounds_of()
        self.assertEqual(box.min, Point(-math.inf, -math.inf, -math.inf))
        self.assertEqual(box.max, Point(math.inf, math.inf, math.inf))

    # Scenario: A bounded cone has a bounding box
    def test_bounded_cone_bounding_box(self):
        shape = Cone()
        shape.minimum = -5
        shape.maximum = 3
        box = shape.bounds_of()
        self.assertEqual(box.min, Point(-5, -5, -5))
        self.assertEqual(box.max, Point(5, 3, 5))

if __name__ == '__main__':
    unittest.main()
