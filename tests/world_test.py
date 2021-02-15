import math
import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from color import Color
from computations import Computations
from intersection import Intersection
from light import PointLight
from ray import Ray
from pattern import Pattern
from plane import Plane
from sphere import Sphere
from transformations import Transformations
from tuple import *
from world import World

class TestWorld(unittest.TestCase):
    # Scenario: Creating a world
    def test_world(self):
        w = World()
        self.assertEqual(w.objects, [])
        self.assertEqual(w.light, None)

    # Scenario: The default world
    def test_default_world(self):
        light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
        s1 = Sphere()
        s1.material.color = Color(0.8, 1.0, 0.6)
        s1.material.diffuse = 0.7
        s1.material.specular = 0.2

        s2 = Sphere()
        s2.transform = Transformations.scaling(0.5, 0.5, 0.5)

        w = World.default_world()
        self.assertEqual(w.light, light)
        self.assertTrue(s1 in w.objects)
        self.assertTrue(s2 in w.objects)

    # Scenario: Intersect a world with a ray
    def test_intersect_world_ray(self):
        w = World.default_world()
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = World.intersect_world(w, r)
        self.assertEqual(len(xs), 4)
        self.assertEqual(xs[0].t, 4)
        self.assertEqual(xs[1].t, 4.5)
        self.assertEqual(xs[2].t, 5.5)
        self.assertEqual(xs[3].t, 6)

    # Scenario: Shading an intersection
    def test_shading_intersection(self):
        w = World.default_world()
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = w.objects[0]
        i = Intersection(4, shape)
        comps = Computations.prepare_computations(i, r)
        c = World.shade_hit(w, comps)
        self.assertEqual(c, Color(0.38066, 0.47583, 0.2855))

    # Scenario: Shading an intersection from the inside
    def test_shade_intersection_inside(self):
        w = World.default_world()
        w.light = PointLight(Point(0, 0.25, 0), Color(1, 1, 1))
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = w.objects[1]
        i = Intersection(0.5, shape)
        comps = Computations.prepare_computations(i, r)
        c = World.shade_hit(w, comps)
        self.assertEqual(c, Color(0.90498, 0.90498, 0.90498))

    # Scenario: The color when a ray misses
    def test_color_ray_miss(self):
        w = World.default_world()
        r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
        c = World.color_at(w, r)
        self.assertEqual(c, Color(0, 0, 0))

    # Scenario: The color when a ray hits
    def test_color_ray_hit(self):
        w = World.default_world()
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        c = World.color_at(w, r)
        self.assertEqual(c, Color(0.38066, 0.47583, 0.2855))

    # Scenario: The color with an intersection behind the ray
    def test_color_intersection_behind_ray(self):
        w = World.default_world()
        outer = w.objects[0]
        outer.material.ambient = 1
        inner = w.objects[1]
        inner.material.ambient = 1
        r = Ray(Point(0, 0, 0.75), Vector(0, 0, -1))
        c = World.color_at(w, r)
        self.assertEqual(c, inner.material.color)

    # Scenario: There is no shadow when nothing is collinear with point and light
    def test_no_shadow_nothing_collinear_with_point_light(self):
        w = World.default_world()
        p = Point(0, 10, 0)
        self.assertEqual(World.is_shadowed(w, p), False)

    # Scenario: The shadow when an object is between the point and the light
    def test_shadow_object_between_point_light(self):
        w = World.default_world()
        p = Point(10, -10, 10)
        self.assertEqual(World.is_shadowed(w, p), True)

    # Scenario: There is no shadow when an object is behind the light
    def test_no_shadow_object_behind_light(self):
        w = World.default_world()
        p = Point(-20, 20, -20)
        self.assertEqual(World.is_shadowed(w, p), False)

    # Scenario: There is no shadow when an object is behind the point
    def test_no_shadow_object_behing_point(self):
        w = World.default_world()
        p = Point(-2, 2, -2)
        self.assertEqual(World.is_shadowed(w, p), False)

    # Scenario: shade_hit() is given an intersection in shadow
    def test_shade_hit_intersection_in_shadow(self):
        w = World()
        w.light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
        s1 = Sphere()
        w.objects.append(s1)
        s2 = Sphere()
        s2.transform = Transformations.translation(0, 0, 10)
        w.objects.append(s2)
        r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
        i = Intersection(4, s2)
        comps = Computations.prepare_computations(i, r)
        c = World.shade_hit(w, comps)
        self.assertEqual(c, Color(0.1, 0.1, 0.1))
  
    # Scenario: The reflected color for a nonreflective material
    def test_reflected_color_nonreflective_material(self):
        w = World.default_world()
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = w.objects[1]
        shape.material.ambient = 1
        i = Intersection(1, shape)
        comps = Computations.prepare_computations(i, r)
        color = World.reflected_color(w, comps)
        self.assertEqual(color, Color(0, 0, 0))

    # Scenario: The reflected color for a reflective material
    def test_reflected_color_for_reflective_material(self):
        w = World.default_world()
        shape = Plane()
        shape.material.reflective = 0.5
        shape.transform = Transformations.translation(0, -1, 0)
        w.objects.append(shape)
        r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
        i = Intersection(math.sqrt(2), shape)
        comps = Computations.prepare_computations(i, r)
        color = World.reflected_color(w, comps)
        self.assertEqual(color, Color(0.19032, 0.2379, 0.14274))

    # Scenario: shade_hit() with a reflective material
    def test_shade_hit_reflective_material(self):
        w = World.default_world()
        shape = Plane()
        shape.material.reflective = 0.5
        shape.transform = Transformations.translation(0, -1, 0)
        w.objects.append(shape)
        r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
        i = Intersection(math.sqrt(2), shape)
        comps = Computations.prepare_computations(i, r)
        color = World.shade_hit(w, comps)
        self.assertEqual(color, Color(0.87677, 0.92436, 0.82918))

    # Scenario: color_at() with mutually reflective surfaces
    def test_color_at_with_mutually_reflective_surfaces(self):
        w = World()
        w.light = PointLight(Point(0, 0, 0), Color(1, 1, 1))
        lower = Plane()
        lower.material.reflective = 1
        lower.transform = Transformations.translation(0, -1, 0)
        w.objects.append(lower)
        upper = Plane()
        upper.material.reflective = 1
        upper.transform = Transformations.translation(0, 1, 0)
        w.objects.append(upper)
        r = Ray(Point(0, 0, 0), Vector(0, 1, 0))
        self.assertIsNotNone(World.color_at(w, r))

    # Scenario: The reflected color at the maximum recursive depth
    def test_reflected_color_at_maximum_recursive_depth(self):
        w = World.default_world()
        shape = Plane()
        shape.material.reflective = 0.5
        shape.transform = Transformations.translation(0, -1, 0)
        w.objects.append(shape)
        r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
        i = Intersection(math.sqrt(2), shape)
        comps = Computations.prepare_computations(i, r)
        color = World.reflected_color(w, comps, 0)
        self.assertEqual(color, Color(0, 0, 0))

    # Scenario: The refracted color with an opaque surface
    def test_refracted_color_with_opaque_surface(self):
        w = World.default_world()
        shape = w.objects[0]
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = Intersection.intersections(Intersection(4, shape), Intersection(6, shape))
        comps = Computations.prepare_computations(xs[0], r, xs)
        c = World.refracted_color(w, comps, 5)
        self.assertEqual(c, Color(0, 0, 0))

    # Scenario: The refracted color at the maximum recursive depth
    def test_refracted_color_at_max_recursive_depth(self):
        w = World.default_world()
        shape = w.objects[0]
        shape.material.transparency = 1.0
        shape.material.refractive_index = 1.5
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = Intersection.intersections(Intersection(4, shape), Intersection(6, shape))
        comps = Computations.prepare_computations(xs[0], r, xs)
        c = World.refracted_color(w, comps, 0)
        self.assertEqual(c, Color(0, 0, 0))

    # Scenario: The refracted color under total internal reflection
    def test_refracted_color_under_total_internal_reflection(self):
        w = World.default_world()
        shape = w.objects[0]
        shape.material.transparency = 1.0
        shape.material.refractive_index = 1.5
        r = Ray(Point(0, 0, math.sqrt(2) / 2), Vector(0, 1, 0))
        xs = Intersection.intersections(Intersection(-math.sqrt(2) / 2, shape), Intersection(math.sqrt(2) / 2, shape))
        # NOTE: this time you're inside the sphere, so you need
        # to look at the second intersection, xs[1], not xs[0]
        comps = Computations.prepare_computations(xs[1], r, xs)
        c = World.refracted_color(w, comps, 5)
        self.assertEqual(c, Color(0, 0, 0))

    # Scenario: The refracted color with a refracted ray
    def test_refracted_color_with_refracted_ray(self):
        w = World.default_world()
        a = w.objects[0]
        a.material.ambient = 1.0
        a.material.pattern = Pattern.test_pattern()
        b = w.objects[1]
        b.material.transparency = 1.0
        b.material.refractive_index = 1.5
        r = Ray(Point(0, 0, 0.1), Vector(0, 1, 0))
        xs = Intersection.intersections(Intersection(-0.9899, a), Intersection(-0.4899, b), Intersection(0.4899, b), Intersection(0.9899, a))
        comps = Computations.prepare_computations(xs[2], r, xs)
        c = World.refracted_color(w, comps, 5)
        self.assertEqual(c, Color(0, 0.99888, 0.04725))

    # Scenario: shade_hit() with a transparent material
    def test_shade_hit_with_transparent_material(self):
        w = World.default_world()
        floor = Plane()
        floor.transform = Transformations.translation(0, -1, 0)
        floor.material.transparency = 0.5
        floor.material.refractive_index = 1.5
        w.objects.append(floor)
        ball = Sphere()
        ball.material.color = Color(1, 0, 0)
        ball.material.ambient = 0.5
        ball.transform = Transformations.translation(0, -3.5, -0.5)
        w.objects.append(ball)
        r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
        xs = Intersection.intersections(Intersection(math.sqrt(2), floor))
        comps = Computations.prepare_computations(xs[0], r, xs)
        color = World.shade_hit(w, comps, 5)
        self.assertEqual(color, Color(0.93642, 0.68642, 0.68642))

    # Scenario: shade_hit() with a reflective, transparent material
    def test_shade_hit_with_reflective_transparent_material(self):
        w = World.default_world()
        r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
        floor = Plane()
        floor.transform = Transformations.translation(0, -1, 0)
        floor.material.reflective = 0.5
        floor.material.transparency = 0.5
        floor.material.refractive_index = 1.5
        w.objects.append(floor)
        ball = Sphere()
        ball.material.color = Color(1, 0, 0)
        ball.material.ambient = 0.5
        ball.transform = Transformations.translation(0, -3.5, -0.5)
        w.objects.append(ball)
        xs = Intersection.intersections(Intersection(math.sqrt(2), floor))
        comps = Computations.prepare_computations(xs[0], r, xs)
        color = World.shade_hit(w, comps, 5)
        self.assertEqual(color, Color(0.93391, 0.69643, 0.69243))
  
if __name__ == '__main__':
    unittest.main()
