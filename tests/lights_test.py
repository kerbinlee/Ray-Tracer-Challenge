import os, sys
import unittest
sys.path.append(os.path.abspath('..'))
from color import Color
from light import PointLight
from tuple import *

class TestLights(unittest.TestCase):
    # Scenario: A point light has a position and intensity
    def test_point_light(self):
        intensity = Color(1, 1, 1)
        position = Point(0, 0, 0)
        light = PointLight(position, intensity)
        self.assertEqual(light.position, position)
        self.assertEqual(light.intensity, intensity)

if __name__ == '__main__':
    unittest.main()
