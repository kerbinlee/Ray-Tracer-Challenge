import math
import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from collections import namedtuple
from cylinder import Cylinder
from ray import Ray
from tuple import *

class TestCylinders(unittest.TestCase):
    # Scenario Outline: A ray misses a cylinder
    def test_ray_misses_cylinder(self):
        cyl = Cylinder()
        rays = [
            Ray(Point(1, 0, 0), Vector(0, 1, 0)),
            Ray(Point(0, 0, 0), Vector(0, 1, 0)),
            Ray(Point(0, 0, -5), Vector(1, 1, 1))
        ]
        for ray in rays:
            direction = Vector.normalize(ray.direction)
            r = Ray(ray.origin, direction)
            xs = cyl.local_intersect(r)
            self.assertEqual(len(xs), 0)

    # Scenario Outline: A ray strikes a cylinder
    def test_ray_strikes_cylinder(self):
        cyl = Cylinder()
        RayIntersection = namedtuple("RayIntersection", ["origin", "direction", "t0", "t1"])
        ray_intersections = [
            RayIntersection(Point(1, 0, -5), Vector(0, 0, 1), 5, 5),
            RayIntersection(Point(0, 0, -5), Vector(0, 0, 1), 4, 6), 
            RayIntersection(Point(0.5, 0, -5), Vector(0.1, 1, 1), 6.80798, 7.08872)
        ]
        for ray_intersection in ray_intersections:
            direction = Vector.normalize(ray_intersection.direction)
            r = Ray(ray_intersection.origin, direction)
            xs = cyl.local_intersect(r)
            self.assertEqual(len(xs), 2)
            self.assertAlmostEqual(xs[0].t, ray_intersection.t0, delta = Constants.epsilon)
            self.assertAlmostEqual(xs[1].t, ray_intersection.t1, delta = Constants.epsilon)

    # Scenario Outline: Normal vector on a cylinder
    def test_normal_vector_on_cylinder(self):
        cyl = Cylinder()
        PointNormal = namedtuple("PointNormal", ["point", "normal"])
        point_normals = [
            PointNormal(Point(1, 0, 0), Vector(1, 0, 0)),
            PointNormal(Point(0, 5, -1), Vector(0, 0, -1)),
            PointNormal(Point(0, -2, 1), Vector(0, 0, 1)),
            PointNormal(Point(-1, 1, 0), Vector(-1, 0, 0))
        ]
        for point_normal in point_normals:
            n = cyl.local_normal_at(point_normal.point)
            self.assertEqual(n, point_normal.normal)

    # Scenario: The default minimum and maximum for a cylinder
    def test_default_minimum_maximum_cylinder(self):
        cyl = Cylinder()
        self.assertEqual(cyl.minimum, -math.inf)
        self.assertEqual(cyl.maximum, math.inf)

    # Scenario Outline: Intersecting a constrained cylinder
    def test_intersect_constrained_cylinder(self):
        cyl = Cylinder()
        cyl.minimum = 1
        cyl.maximum = 2
        CylinderIntersection = namedtuple("CyliderIntersection", ["point", "direction", "count"])
        cylinder_intersections = [
            CylinderIntersection(Point(0, 1.5, 0), Vector(0.1, 1, 0), 0),
            CylinderIntersection(Point(0, 3, -5), Vector(0, 0, 1), 0),
            CylinderIntersection(Point(0, 0, -5), Vector(0, 0, 1), 0),
            CylinderIntersection(Point(0, 2, -5), Vector(0, 0, 1), 0),
            CylinderIntersection(Point(0, 1, -5), Vector(0, 0, 1), 0),
            CylinderIntersection(Point(0, 1.5, -2), Vector(0, 0, 1), 2)
        ]
        for cylinder_intersection in cylinder_intersections:
            direction = Vector.normalize(cylinder_intersection.direction)
            r = Ray(cylinder_intersection.point, direction)
            xs = cyl.local_intersect(r)
            self.assertEqual(len(xs), cylinder_intersection.count)

    # Scenario: The default closed value for a cylinder
    def test_cylinder_default_closed_value(self):
        cyl = Cylinder()
        self.assertFalse(cyl.closed)

    # Scenario Outline: Intersecting the caps of a closed cylinder
    def test_interserct_caps_of_closed_cylinder(self):
        cyl = Cylinder()
        cyl.minimum = 1
        cyl.maximum = 2
        cyl.closed = True
        cyl.maximum = 2
        CylinderIntersection = namedtuple("CyliderIntersection", ["point", "direction", "count"])
        cylinder_intersections = [
            CylinderIntersection(Point(0, 3, 0), Vector(0, -1, 0), 2),
            CylinderIntersection(Point(0, 3, -2), Vector(0, -1, 2), 2),
            CylinderIntersection(Point(0, 4, -2), Vector(0, -1, 1), 2), # corner case
            CylinderIntersection(Point(0, 0, -2), Vector(0, 1, 2) , 2),
            CylinderIntersection(Point(0, -1, -2), Vector(0, 1, 1) , 2) # corner case
        ]
        for cylinder_intersection in cylinder_intersections:
            direction = Vector.normalize(cylinder_intersection.direction)
            r = Ray(cylinder_intersection.point, direction)
            xs = cyl.local_intersect(r)
            self.assertEqual(len(xs), cylinder_intersection.count)

    # Scenario Outline: The normal vector on a cylinder's end caps
    def test_normal_vector_cylinder_end_caps(self):
        cyl = Cylinder()
        cyl.minimum = 1
        cyl.maximum = 2
        cyl.closed = True
        PointNormal = namedtuple("PointNormal", ["point", "normal"])
        point_normals = [
            PointNormal(Point(0, 1, 0), Vector(0, -1, 0)),
            PointNormal(Point(0.5, 1, 0), Vector(0, -1, 0)),
            PointNormal(Point(0, 1, 0.5), Vector(0, -1, 0)),
            PointNormal(Point(0, 2, 0), Vector(0, 1, 0)),
            PointNormal(Point(0.5, 2, 0), Vector(0, 1, 0)),
            PointNormal(Point(0, 2, 0.5), Vector(0, 1, 0))
        ]
        for point_normal in point_normals:
            n = cyl.local_normal_at(point_normal.point)
            self.assertEqual(n, point_normal.normal)

    # Scenario: An unbounded cylinder has a bounding box
    def test_unbounded_cylinder_bounding_box(self):
        shape = Cylinder()
        box = shape.bounds_of()
        self.assertEqual(box.min, Point(-1, -math.inf, -1))
        self.assertEqual(box.max, Point(1, math.inf, 1))

    # Scenario: A bounded cylinder has a bounding box
    def test_bounded_cylinder_bounding_box(self):
        shape = Cylinder()
        shape.minimum = -5
        shape.maximum = 3
        box = shape.bounds_of()
        self.assertEqual(box.min, Point(-1, -5, -1))
        self.assertEqual(box.max, Point(1, 3, 1))
        
if __name__ == '__main__':
    unittest.main()
