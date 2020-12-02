import math
import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from matrix import Matrix
from tuple import *
from transformations import Transformations

class TestMatrices(unittest.TestCase):
    def test_multiply_translation_matrix(self):
        transform = Transformations.translation(5, -3, 2)
        p = Point(-3, 4, 5)
        self.assertEqual(Matrix.multiply_tuple(transform, p), Point(2, 1, 7))

    def test_multiply_inverse_translation_matrix(self):
        transform = Transformations.translation(5, -3, 2)
        inv = Matrix.inverse(transform)
        p = Point(-3, 4, 5)
        self.assertTrue(Matrix.multiply_tuple(inv, p), Point(-8, 7, 3))

    def test_translation_vectors(self):
        transform = Transformations.translation(5, -3, 2)
        v = Vector(-3, 4, 5)
        self.assertEqual(Matrix.multiply_tuple(transform, v), v)

    def test_scaling_matrix_point(self):
        transform = Transformations.scaling(2, 3, 4)
        p = Point(-4, 6, 8)
        self.assertEqual(Matrix.multiply_tuple(transform, p), Point(-8, 18, 32))

    def test_scaling_matrix_vector(self):
        transform = Transformations.scaling(2, 3, 4)
        v = Vector(-4, 6, 8)
        self.assertEqual(Matrix.multiply_tuple(transform, v), Vector(-8, 18, 32))

    def test_multiply_inverse_scaling_matrix(self):
        transform = Transformations.scaling(2, 3, 4)
        inv = Matrix.inverse(transform)
        v = Vector(-4, 6, 8)
        self.assertEqual(Matrix.multiply_tuple(inv, v), Vector(-2, 2, 2))

    def test_reflection(self):
        transform = Transformations.scaling(-1, 1, 1)
        p = Point(2, 3, 4)
        self.assertEqual(Matrix.multiply_tuple(transform, p), Point(-2, 3, 4))

    def test_rotate_point_x(self):
        p = Point(0, 1, 0)
        half_quarter = Transformations.rotation_x(math.pi / 4)
        full_quarter = Transformations.rotation_x(math.pi / 2)
        self.assertEqual(Matrix.multiply_tuple(half_quarter, p), Point(0, math.sqrt(2) / 2, math.sqrt(2) / 2))
        self.assertEqual(Matrix.multiply_tuple(full_quarter, p), Point(0, 0, 1))

    def test_rotate_point_x_inverse(self):
        p = Point(0, 1, 0)
        half_quarter = Transformations.rotation_x(math.pi / 4)
        inv = Matrix.inverse(half_quarter)
        self.assertEqual(Matrix.multiply_tuple(inv, p), Point(0, math.sqrt(2) / 2, -math.sqrt(2) / 2))

    def test_rotate_point_y(self):
        p = Point(0, 0, 1)
        half_quarter = Transformations.rotation_y(math.pi / 4)
        full_quarter = Transformations.rotation_y(math.pi / 2)
        self.assertEqual(Matrix.multiply_tuple(half_quarter, p), Point(math.sqrt(2) / 2, 0, math.sqrt(2) / 2))
        self.assertEqual(Matrix.multiply_tuple(full_quarter, p), Point(1, 0, 0))

    def test_rotate_point_z(self):
        p = Point(0, 1, 0)
        half_quarter = Transformations.rotation_z(math.pi / 4)
        full_quarter = Transformations.rotation_z(math.pi / 2)
        self.assertEqual(Matrix.multiply_tuple(half_quarter, p), Point(-math.sqrt(2) / 2, math.sqrt(2) / 2, 0))
        self.assertEqual(Matrix.multiply_tuple(full_quarter, p), Point(-1, 0, 0))

    def test_shearing_x_y(self):
        transform = Transformations.shearing(1, 0, 0, 0, 0, 0)
        p = Point(2, 3, 4)
        self.assertEqual(Matrix.multiply_tuple(transform, p), Point(5, 3, 4))

    def test_shearing_x_z(self):
        transform = Transformations.shearing(0, 1, 0, 0, 0, 0)
        p = Point(2, 3, 4)
        self.assertEqual(Matrix.multiply_tuple(transform, p), Point(6, 3, 4))

    def test_shearing_y_x(self):
        transform = Transformations.shearing(0, 0, 1, 0, 0, 0)
        p = Point(2, 3, 4)
        self.assertEqual(Matrix.multiply_tuple(transform, p), Point(2, 5, 4))

    def test_shearing_y_z(self):
        transform = Transformations.shearing(0, 0, 0, 1, 0, 0)
        p = Point(2, 3, 4)
        self.assertEqual(Matrix.multiply_tuple(transform, p), Point(2, 7, 4))

    def test_shearing_z_x(self):
        transform = Transformations.shearing(0, 0, 0, 0, 1, 0)
        p = Point(2, 3, 4)
        self.assertEqual(Matrix.multiply_tuple(transform, p), Point(2, 3, 6))

    def test_shearing_z_y(self):
        transform = Transformations.shearing(0, 0, 0, 0, 0, 1)
        p = Point(2, 3, 4)
        self.assertEqual(Matrix.multiply_tuple(transform, p), Point(2, 3, 7))

    def test_individual_transformations(self):
        p = Point(1, 0, 1)
        a = Transformations.rotation_x(math.pi / 2)
        b = Transformations.scaling(5, 5, 5)
        c = Transformations.translation(10, 5, 7)
        # rotate first
        p2 = Matrix.multiply_tuple(a, p)
        self.assertEqual(p2, Point(1, -1, 0))
        # apply scaling
        p3 = Matrix.multiply_tuple(b, p2)
        self.assertEqual(p3, Point(5, -5, 0))
        # apply translation
        p4 = Matrix.multiply_tuple(c, p3)
        self.assertEqual(p4, Point(15, 0, 7))

    def test_chained_transformations(self):
        p = Point(1, 0, 1)
        a = Transformations.rotation_x(math.pi / 2)
        b = Transformations.scaling(5, 5, 5)
        c = Transformations.translation(10, 5, 7)
        t = c.dot(b.dot(a))
        self.assertEqual(Matrix.multiply_tuple(t, p), Point(15, 0, 7))

if __name__ == '__main__':
    unittest.main()
