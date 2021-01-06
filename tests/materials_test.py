import math
import os, sys
import unittest
sys.path.append(os.path.abspath('..'))
from color import Color
from light import PointLight
from material import Material
from tuple import *

class TestMaterial(unittest.TestCase):
    # Background
    # @classmethod
    # def setUpClass(cls):
    #     m = Material()
    #     position = Point(0, 0, 0)

    # Scenario: The default material
    def test_default_material(self):
        m = Material()
        self.assertEqual(m.color, Color(1, 1, 1))
        self.assertEqual(m.ambient, 0.1)
        self.assertEqual(m.diffuse, 0.9)
        self.assertEqual(m.specular, 0.9)
        self.assertEqual(m.shininess, 200.0)

    # Scenario: Lighting with the eye between the light and the surface
    def test_light_eye_light_surface(self):
        m = Material()
        position = Point(0, 0, 0)
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
        result = PointLight.lighting(m, light, position, eyev, normalv)
        self.assertEqual(result, Color(1.9, 1.9, 1.9))

    # Scenario: Lighting with the eye between light and surface, eye offset 45°
    def test_light_eye_45_light_surface(self):
        m = Material()
        position = Point(0, 0, 0)
        eyev = Vector(0, math.sqrt(2) / 2, -math.sqrt(2) / 2)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
        result = PointLight.lighting(m, light, position, eyev, normalv)
        self.assertEqual(result, Color(1.0, 1.0, 1.0))

    # Scenario: Lighting with eye opposite surface, light offset 45°
    def test_light_45_surface_eye(self):
        m = Material()
        position = Point(0, 0, 0)
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
        result = PointLight.lighting(m, light, position, eyev, normalv)
        self.assertEqual(result, Color(0.7364, 0.7364, 0.7364))

    # Scenario: Lighting with eye in the path of the reflection vector
    def test_light_eye_reflection(self):
        m = Material()
        position = Point(0, 0, 0)
        eyev = Vector(0, -math.sqrt(2) / 2, -math.sqrt(2) / 2)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
        result = PointLight.lighting(m, light, position, eyev, normalv)
        self.assertEqual(result, Color(1.6364, 1.6364, 1.6364))

    # Scenario: Lighting with the light behind the surface
    def test_light_behind_surface(self):
        m = Material()
        position = Point(0, 0, 0)
        eyev = Vector(0, 0, -1)
        normalv = Vector(0, 0, -1)
        light = PointLight(Point(0, 0, 10), Color(1, 1, 1))
        result = PointLight.lighting(m, light, position, eyev, normalv)
        self.assertEqual(result, Color(0.1, 0.1, 0.1))

if __name__ == '__main__':
    unittest.main()
