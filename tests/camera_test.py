import math
import os, sys
import unittest

import numpy as np

sys.path.append(os.path.abspath('..'))
from camera import Camera
from canvas import Canvas
from color import Color
from transformations import Transformations
from tuple import *
from world import World

class TestCamera(unittest.TestCase):
    # Scenario: Constructing a camera
    def test_constructing_camera(self):
        hsize = 160
        vsize = 120
        field_of_view = math.pi / 2
        c = Camera(hsize, vsize, field_of_view)
        self.assertEqual(c.hsize, 160)
        self.assertEqual(c.vsize, 120)
        self.assertEqual(c.field_of_view, math.pi / 2)
        self.assertTrue(np.array_equal(c.transform, np.identity(4)))

    # Scenario: The pixel size for a horizontal canvas
    def test_pixel_size_horizontal_canvas(self):
        c = Camera(200, 125, math.pi / 2)
        self.assertAlmostEqual(c.pixel_size, 0.01, delta = Constants.epsilon)

    # Scenario: The pixel size for a vertical canvas
    def test_pixel_size_vertical_canvas(self):
        c = Camera(125, 200, math.pi / 2)
        self.assertAlmostEqual(c.pixel_size, 0.01, delta = Constants.epsilon)

    # Scenario: Constructing a ray through the center of the canvas
    def test_ray_through_center_canvas(self):
        c = Camera(201, 101, math.pi / 2)
        r = Camera.ray_for_pixel(c, 100, 50)
        self.assertEqual(r.origin, Point(0, 0, 0))
        self.assertEqual(r.direction, Vector(0, 0, -1))

    # Scenario: Constructing a ray through a corner of the canvas
    def test_ray_through_corner_canvas(self):
        c = Camera(201, 101, math.pi / 2)
        r = Camera.ray_for_pixel(c, 0, 0)
        self.assertEqual(r.origin, Point(0, 0, 0))
        self.assertEqual(r.direction, Vector(0.66519, 0.33259, -0.66851))

    # Scenario: Constructing a ray when the camera is transformed
    def test_ray_camera_transformed(self):
        c = Camera(201, 101, math.pi / 2)
        c.transform = Transformations.rotation_y(math.pi / 4).dot(Transformations.translation(0, -2, 5))
        r = Camera.ray_for_pixel(c, 100, 50)
        self.assertEqual(r.origin, Point(0, 2, -5))
        self.assertEqual(r.direction, Vector(math.sqrt(2) / 2, 0, -math.sqrt(2) / 2))

    # Scenario: Rendering a world with a camera
    def test_render_world_camera(self):
        w = World.default_world()
        c = Camera(11, 11, math.pi / 2)
        from_point = Point(0, 0, -5)
        to = Point(0, 0, 0)
        up = Vector(0, 1, 0)
        c.transform = World.view_transform(from_point, to, up)
        image = Camera.render(c, w)
        self.assertEqual(Canvas.pixel_at(image, 5, 5), Color(0.38066, 0.47583, 0.2855))

if __name__ == '__main__':
    unittest.main()
    