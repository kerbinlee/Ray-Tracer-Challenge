import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from color import Color
from computations import Computations
from intersection import Intersection
from light import PointLight
from ray import Ray
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
  
if __name__ == '__main__':
    unittest.main()
