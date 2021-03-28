import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from collections import namedtuple
from cube import Cube
from ray import Ray
from tuple import *

class TestCubes(unittest.TestCase):
    # Scenario Outline: A ray intersects a cube
    def test_ray_intersect_cube(self):
        c = Cube()
        Intersections = namedtuple("Intersections", ["origin", "direction", "t1", "t2"])
        intersections_list = [
            Intersections(Point(5, 0.5, 0), Vector(-1, 0, 0), 4,  6),
            Intersections(Point(-5, 0.5, 0), Vector(1, 0, 0), 4,  6),
            Intersections(Point(0.5, 5, 0), Vector(0, -1, 0), 4,  6),
            Intersections(Point(0.5, -5, 0), Vector(0, 1, 0), 4,  6),
            Intersections(Point(0.5, 0, 5), Vector(0, 0, -1), 4,  6),
            Intersections(Point(0.5, 0, -5), Vector(0, 0, 1), 4,  6),
            Intersections(Point(0, 0.5, 0), Vector(0, 0, 1), -1,  1)
        ]
        for intersection in intersections_list:
            r = Ray(intersection.origin, intersection.direction)
            xs = c.local_intersect(r)
            self.assertEqual(len(xs), 2)
            self.assertEqual(xs[0].t, intersection.t1)
            self.assertEqual(xs[1].t, intersection.t2)

    # Scenario Outline: A ray misses a cube
    def test_ray_misses_cube(self):
        c = Cube()
        rays = [
            Ray(Point(-2, 0, 0), Vector(0.2673, 0.5345, 0.8018)),
            Ray(Point(0, -2, 0), Vector(0.8018, 0.2673, 0.5345)),
            Ray(Point(0, 0, -2), Vector(0.5345, 0.8018, 0.2673)),
            Ray(Point(2, 0, 2), Vector(0, 0, -1)),
            Ray(Point(0, 2, 2), Vector(0, -1, 0)),
            Ray(Point(2, 2, 0), Vector(-1, 0, 0))
        ]
        for ray in rays:
            r = Ray(ray.origin, ray.direction)
            xs = c.local_intersect(r)
            self.assertEqual(len(xs), 0)

    # Scenario Outline: The normal on the surface of a cube
    def test_normal_on_surface_cube(self):
        c = Cube()
        PointNormal = namedtuple("PointNormal", ["point", "normal"])
        point_normal_list = [
            PointNormal(Point(1, 0.5, -0.8), Vector(1, 0, 0)),
            PointNormal(Point(-1, -0.2, 0.9), Vector(-1, 0, 0)),
            PointNormal(Point(-0.4, 1, -0.1), Vector(0, 1, 0)),
            PointNormal(Point(0.3, -1, -0.7), Vector(0, -1, 0)),
            PointNormal(Point(-0.6, 0.3, 1), Vector(0, 0, 1)),
            PointNormal(Point(0.4, 0.4, -1), Vector(0, 0, -1)),
            PointNormal(Point(1, 1, 1), Vector(1, 0, 0)),
            PointNormal(Point(-1, -1, -1), Vector(-1, 0, 0))
        ]
        for point_normal in point_normal_list:
            p = point_normal.point
            normal = c.local_normal_at(p)
            self.assertEqual(normal, point_normal.normal)

    # Scenario: A cube has a bounding box
    def test_cube_bounding_box(self):
        shape = Cube()
        box = shape.bounds_of()
        self.assertEqual(box.min, Point(-1, -1, -1))
        self.assertEqual(box.max, Point(1, 1, 1))

if __name__ == '__main__':
    unittest.main()
    