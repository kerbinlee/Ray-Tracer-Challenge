import math
import numpy as np
import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from group import Group
from material import Material
from ray import Ray
from shape import Shape
from sphere import Sphere
from transformations import Transformations
from tuple import *

class TestShapes(unittest.TestCase):
    # Scenario: The default transformation
    def test_default_transformation(self):
        s = Shape.test_shape()
        self.assertTrue(np.array_equal(s.transform, np.identity(4)))

    # Scenario: Assigning a transformation
    def test_assign_transformation(self):
        s = Shape.test_shape()
        s.transform = Transformations.translation(2, 3, 4)
        self.assertTrue(np.array_equiv(s.transform, Transformations.translation(2, 3, 4)))

    # Scenario: The default material
    def test_default_material(self):
        s = Shape.test_shape()
        m = s.material
        self.assertEqual(m, Material())

    # Scenario: Assigning a material
    def test_assign_material(self):
        s = Shape.test_shape()
        m = Material()
        m.ambient = 1
        s.material = m
        self.assertEqual(s.material, m)

    # Scenario: Intersecting a scaled shape with a ray
    def test_intersect_scaled_shape_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Shape.test_shape()
        s.transform = Transformations.scaling(2, 2, 2)
        xs = s.intersect(r)
        self.assertEqual(s.saved_ray.origin, Point(0, 0, -2.5))
        self.assertEqual(s.saved_ray.direction, Vector(0, 0, 0.5))
    
    # Scenario: Intersecting a translated shape with a ray
    def test_intersect_translated_shape_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Shape.test_shape()
        s.transform = Transformations.translation(5, 0, 0)
        xs = s.intersect(r)
        self.assertEqual(s.saved_ray.origin, Point(-5, 0, -5))
        self.assertEqual(s.saved_ray.direction, Vector(0, 0, 1))

    # Scenario: Computing the normal on a translated shape
    def test_normal_translated_shape(self):
        s = Shape.test_shape()
        s.transform = Transformations.translation(0, 1, 0)
        n = s.normal_at(Point(0, 1.70711, -0.70711))
        n = Vector(0, 0.70711, -0.70711)

    # Scenario: Computing the normal on a transformed shape
    def test_normal_transformed_shape(self):
        s = Shape.test_shape()
        m = Transformations.scaling(1, 0.5, 1).dot(Transformations.rotation_z(math.pi / 5))
        s.transform = m
        n = s.normal_at(Point(0, math.sqrt(2) / 2, -math.sqrt(2) / 2))
        n = Vector(0, 0.97014, -0.24254)

    # Scenario: Test Sphere is a Shape
    def test_sphere_shape(self):
        s = Sphere()
        self.assertIsInstance(s, Shape)

    # Scenario: A shape has a parent attribute
    def test_shape_has_parent_attribute(self):
        s = Shape.test_shape()
        self.assertIsNone(s.parent)

    # Scenario: Converting a point from world to object space
    def test_converting_point_from_world_to_object_space(self):
        g1 = Group()
        g1.transform = Transformations.rotation_y(math.pi / 2)
        g2 = Group()
        g2.transform = Transformations.scaling(2, 2, 2)
        g1.add_child(g2)
        s = Sphere()
        s.transform = Transformations.translation(5, 0, 0)
        g2.add_child(s)
        p = s.world_to_object(Point(-2, 0, -10))
        self.assertEqual(p, Point(0, 0, -1))

    # Scenario: Converting a normal from object to world space
    def test_converting_normal_from_object_to_world_space(self):
        g1 = Group()
        g1.transform = Transformations.rotation_y(math.pi / 2)
        g2 = Group()
        g2.transform = Transformations.scaling(1, 2, 3)
        g1.add_child(g2)
        s = Sphere()
        s.transform = Transformations.translation(5, 0, 0)
        g2.add_child(s)
        n = s.normal_to_world(Vector(math.sqrt(3) /3, math.sqrt(3) / 3, math.sqrt(3) / 3))
        self.assertEqual(n, Vector(0.2857, 0.4286, -0.8571))

    # Scenario: Finding the normal on a child object
    def test_finding_normal_on_child_object(self):
        g1 = Group()
        g1.transform = Transformations.rotation_y(math.pi / 2)
        g2 = Group()
        g2.transform = Transformations.scaling(1, 2, 3)
        g1.add_child(g2)
        s = Sphere()
        s.transform = Transformations.translation(5, 0, 0)
        g2.add_child(s)
        n = s.normal_at(Point(1.7321, 1.1547, -5.5774))
        self.assertEqual(n, Vector(0.2857, 0.4286, -0.8571))

if __name__ == '__main__':
    unittest.main()
