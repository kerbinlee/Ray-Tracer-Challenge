import os, sys
import unittest
sys.path.append(os.path.abspath('..'))
from canvas import *

class TestColor(unittest.TestCase):
    def test_canvas(self):
        c = Canvas(10, 20)
        self.assertEqual(c.width, 10)
        self.assertEqual(c.height, 20)
        black = Color(0, 0, 0)
        for x in range(10):
            for y in range(20):
                self.assertEqual(c.pixels[y][x], black)

    def test_pixel_write(self):
        c = Canvas(10, 20)
        red = Color(1, 0, 0)
        c.write_pixel(2, 3, red)
        self.assertEqual(c.pixel_at(2, 3), red)
        black = Color(0, 0, 0)
        for x in range(10):
            for y in range(20):
                if x != 2 and y != 3:
                    self.assertEqual(c.pixel_at(x, y), black)

    def test_canvas_to_ppm_header(self):
        c = Canvas(5, 3)
        c.canvas_to_ppm()
        with open("canvas.ppm", "r") as ppm_file: 
            self.assertEqual(ppm_file.readline(), "P3\n")
            self.assertEqual(ppm_file.readline(), "5 3\n")
            self.assertEqual(ppm_file.readline(), "255\n")
            #TODO: check for end of file

    def test_canvas_to_ppm(self):
        c = Canvas(5, 3)
        c1 = Color(1.5, 0, 0)
        c2 = Color(0, 0.5, 0)
        c3 = Color(-0.5, 0, 1)
        c.write_pixel(0, 0, c1)
        c.write_pixel(2, 1, c2)
        c.write_pixel(4, 2, c3)
        c.canvas_to_ppm()
        with open("canvas.ppm", "r") as ppm_file:
            for _ in range(3):
                ppm_file.readline()
            self.assertEqual(ppm_file.readline(), "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n")
            self.assertEqual(ppm_file.readline(), "0 0 0 0 0 0 0 128 0 0 0 0 0 0 0\n")
            self.assertEqual(ppm_file.readline(), "0 0 0 0 0 0 0 0 0 0 0 0 0 0 255\n")
            # TODO: check for end of file

    def test_ppm_long_lines(self):
        c = Canvas(10, 2)
        color = Color(1, 0.8, 0.6)
        for x in range(10):
            for y in range(2):
                c.write_pixel(x, y, color)
        c.canvas_to_ppm()
        with open("canvas.ppm", "r") as ppm_file:
            for _ in range(3):
                ppm_file.readline()
            self.assertEqual(ppm_file.readline(), "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204\n")
            self.assertEqual(ppm_file.readline(), "153 255 204 153 255 204 153 255 204 153 255 204 153\n")
            self.assertEqual(ppm_file.readline(), "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204\n")
            self.assertEqual(ppm_file.readline(), "153 255 204 153 255 204 153 255 204 153 255 204 153\n")

    def test_ppm_newline_terminator(self):
        c = Canvas(5, 3)
        c.canvas_to_ppm()
        with open("canvas.ppm", "r") as ppm_file:
            for _ in range(6):
                ppm_file.readline()
            self.assertEqual(ppm_file.readline(), "\n")

if __name__ == '__main__':
    unittest.main()