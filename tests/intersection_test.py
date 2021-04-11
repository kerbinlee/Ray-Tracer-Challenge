import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from collections import namedtuple
from computations import Computations
from intersection import Intersection
from plane import Plane
from ray import Ray
from sphere import GlassSphere, Sphere
from transformations import Transformations
from triangle import Triangle
from tuple import *
from world import World

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

    # Scenario: Precomputing the state of an intersection
    def test_precompute_state_intersection(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(4, shape)
        comps = Computations.prepare_computations(i, r)
        self.assertEqual(comps.t, i.t)
        self.assertEqual(comps.object, i.object)
        self.assertEqual(comps.point, Point(0, 0, -1))
        self.assertEqual(comps.eyev, Vector(0, 0, -1))
        self.assertEqual(comps.normalv, Vector(0, 0, -1))

    # Scenario: The hit, when an intersection occurs on the outside
    def test_hit_outside(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(4, shape)
        comps = Computations.prepare_computations(i, r)
        self.assertFalse(comps.inside)

    # Scenario: The hit, when an intersection occurs on the inside
    def test_hit_inside(self):
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(1, shape)
        comps = Computations.prepare_computations(i, r)
        self.assertEqual(comps.point, Point(0, 0, 1))
        self.assertEqual(comps.eyev, Vector(0, 0, -1))
        self.assertTrue(comps.inside)
        # normal would have been (0, 0, 1), but is inverted!
        self.assertEqual(comps.normalv, Vector(0, 0, -1))

    # Scenario: The hit should offset the point
    def test_hit_offset_point(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        shape.transform = Transformations.translation(0, 0, 1)
        i = Intersection(5, shape)
        comps = Computations.prepare_computations(i, r)
        self.assertLess(comps.over_point.z, -Constants.epsilon / 2)
        self.assertGreater(comps.point.z, comps.over_point.z)

    # Scenario: Precomputing the reflection vector
    def test_precomputing_reflection_vector(self):
        shape = Plane()
        r = Ray(Point(0, 1, -1), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2)) 
        i = Intersection(math.sqrt(2), shape)                      
        comps = Computations.prepare_computations(i, r)
        self.assertEqual(comps.reflectv, Vector(0, math.sqrt(2) / 2, math.sqrt(2) / 2))

    # Scenario Outline: Finding n1 and n2 at various intersections
    def test_findinf_n1_n2_at_various_intersections(self):
        a = GlassSphere()
        a.transform = Transformations.scaling(2, 2, 2)
        a.material.refractive_index = 1.5
        b = GlassSphere()
        b.transform = Transformations.translation(0, 0, -0.25)
        b.material.refractive_index = 2.0
        c = GlassSphere()
        c.transform = Transformations.translation(0, 0, 0.25)
        c.material.refractive_index = 2.5
        r = Ray(Point(0, 0, -4), Vector(0, 0, 1))
        xs = Intersection.intersections(Intersection(2, a), Intersection(2.75, b), Intersection(3.25, c), Intersection(4.75, b), Intersection(5.25, c), Intersection(6, a))
        RefractiveIndices = namedtuple("RefractiveIndices", ["n1", "n2"])
        refractive_indices_list = [
            RefractiveIndices(1.0, 1.5),
            RefractiveIndices(1.5, 2.0),
            RefractiveIndices(2.0, 2.5),
            RefractiveIndices(2.5, 2.5),
            RefractiveIndices(2.5, 1.5),
            RefractiveIndices(1.5, 1.0)
        ]
        for index, refractive_index in enumerate(refractive_indices_list):
            comps = Computations.prepare_computations(xs[index], r, xs)
            print(comps.n1)
            print(comps.n2)
            self.assertEqual(comps.n1, refractive_index.n1)
            self.assertEqual(comps.n2, refractive_index.n2)

    # Scenario: The under point is offset below the surface
    def test_under_point_offset_below_surface(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = GlassSphere()
        shape.transform = Transformations.translation(0, 0, 1)
        i = Intersection(5, shape)
        xs = Intersection.intersections(i)
        comps = Computations.prepare_computations(i, r, xs)
        self.assertGreater(comps.under_point.z, Constants.epsilon / 2)
        self.assertLess(comps.point.z, comps.under_point.z)

    # Scenario: The Schlick approximation under total internal reflection
    def test_schlick_approximation_under_total_internal_reflection(self):
        shape = GlassSphere()
        r = Ray(Point(0, 0, math.sqrt(2) / 2), Vector(0, 1, 0))
        xs = Intersection.intersections(Intersection(-math.sqrt(2) / 2, shape), Intersection(math.sqrt(2) / 2, shape))
        comps = Computations.prepare_computations(xs[1], r, xs)
        reflectance = World.schlick(comps)
        self.assertEqual(reflectance, 1.0)

    # Scenario: The Schlick approximation with a perpendicular viewing angle
    def test_schlick_approximation_with_perpendicular_viewing_angle(self):
        shape = GlassSphere()
        r = Ray(Point(0, 0, 0), Vector(0, 1, 0))
        xs = Intersection.intersections(Intersection(-1,shape), Intersection(1, shape))
        comps = Computations.prepare_computations(xs[1], r, xs)
        reflectance = World.schlick(comps)
        self.assertAlmostEqual(reflectance, 0.04, delta = Constants.epsilon)

    # Scenario: The Schlick approximation with small angle and n2 > n1
    def test_schlick_approximation_with_small_angle(self):
        shape = GlassSphere()
        r = Ray(Point(0, 0.99, -2), Vector(0, 0, 1))
        xs = Intersection.intersections(Intersection(1.8589, shape))
        comps = Computations.prepare_computations(xs[0], r, xs)
        reflectance = World.schlick(comps)
        self.assertAlmostEqual(reflectance, 0.48873, delta = Constants.epsilon)

    # Scenario: An intersection can encapsulate `u` and `v`
    def test_intersection_u_v(self):
        s = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
        i = Intersection(3.5, s, 0.2, 0.4)
        self.assertEqual(i.u, 0.2)
        self.assertEqual(i.v, 0.4)

if __name__ == '__main__':
    unittest.main()
