import math
import numpy as np
import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from transformations import Transformations
from tuple import *
from sphere import Sphere, GlassSphere
from ray import Ray

class TestSphere(unittest.TestCase):
    # Scenario: A ray intersects a sphere at two points
    def test_ray_intersect_sphere_two_points(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, 4.0)
        self.assertEqual(xs[1].t, 6.0)

    # Scenario: A ray intersects a sphere at a tangent
    def test_ray_intersect_sphere_tangent(self):
        r = Ray(Point(0, 1, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, 5.0)
        self.assertEqual(xs[1].t, 5.0)

    # Scenario: A ray misses a sphere
    def test_ray_miss_sphere(self):
        r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(len(xs), 0)
        
    # Scenario: A ray originates inside a sphere
    def test_ray_originate_inside_sphere(self):
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, -1.0)
        self.assertEqual(xs[1].t, 1.0)

    # Scenario: A sphere is behind a ray
    def test_sphere_behind_ray(self):
        r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, -6.0)
        self.assertEqual(xs[1].t, -4.0)

    # Scenario: Intersect sets the object on the intersection
    def test_intersect_object(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].object, s)
        self.assertEqual(xs[1].object, s)

    # Scenario: Intersecting a scaled sphere with a ray
    def test_intersect_scaled_sphere_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        s.transform = Transformations.scaling(2, 2, 2)
        xs = s.intersect(r)
        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, 3)
        self.assertEqual(xs[1].t, 7)

    # Scenario: Intersecting a translated sphere with a ray
    def test_intersect_translated_sphere(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        s.transform = Transformations.translation(5, 0, 0)
        xs = s.intersect(r)
        self.assertEqual(len(xs), 0)

    # Scenario: The normal on a sphere at a point on the x axis
    def test_normal_sphere_x(self):
        s = Sphere()
        n = s.normal_at(Point(1, 0, 0))
        self.assertEqual(n, Vector(1, 0, 0))

    # Scenario: The normal on a sphere at a point on the y axis
    def test_normal_sphere_y(self):
        s = Sphere()
        n = s.normal_at(Point(0, 1, 0))
        self.assertEqual(n, Vector(0, 1, 0))

    # Scenario: The normal on a sphere at a point on the z axis
    def test_normal_sphere_z(self):
        s = Sphere()
        n = s.normal_at(Point(0, 0, 1))
        self.assertEqual(n, Vector(0, 0, 1))

    # Scenario: The normal on a sphere at a nonaxial point
    def test_normal_sphere_nonaxial(self):
        s = Sphere()
        n = s.normal_at(Point(math.sqrt(3) / 3, math.sqrt(3) / 3, math.sqrt(3) / 3))
        self.assertEqual(n, Vector(math.sqrt(3) / 3, math.sqrt(3) / 3, math.sqrt(3) / 3))

    # Scenario: The normal is a normalized vector
    def test_normalized_vector(self):
        s = Sphere()
        n = s.normal_at(Point(math.sqrt(3) / 3, math.sqrt(3) / 3, math.sqrt(3) / 3))
        self.assertEqual(n, Tuple.normalize(n))

    # Scenario: Computing the normal on a translated sphere
    def test_normal_translated_sphere(self):
        s = Sphere()
        s.transform = Transformations.translation(0, 1, 0)
        n = s.normal_at(Point(0, 1.70711, -0.70711))
        self.assertEqual(n, Vector(0, 0.70711, -0.70711))

    # Scenario: Computing the normal on a transformed sphere
    def test_normal_transformed_sphere(self):
        s = Sphere()
        m = Transformations.scaling(1, 0.5, 1).dot(Transformations.rotation_z(math.pi / 5))
        s.transform = m
        n = s.normal_at(Point(0, math.sqrt(2) / 2, -(math.sqrt(2) / 2)))
        self.assertEqual(n, Vector(0, 0.97014, -0.24254))

    # Scenario: A helper for producing a sphere with a glassy material
    def test_sphere_glassy_material(self):
        s = GlassSphere()
        self.assertTrue(np.array_equal(s.transform, np.identity(4)))
        self.assertEqual(s.material.transparency, 1.0)
        self.assertEqual(s.material.refractive_index, 1.5)

    # Scenario: A sphere has a bounding box
    def test_sphere_bounding_box(self):
        shape = Sphere()
        box = shape.bounds_of()
        self.assertEqual(box.min, Point(-1, -1, -1))
        self.assertEqual(box.max, Point(1, 1, 1))

if __name__ == '__main__':
    unittest.main()
