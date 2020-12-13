import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
import numpy as np
from constants import Constants
from matrix import Matrix
from tuple import Tuple

class TestMatrices(unittest.TestCase):
    def test_4x4_matrix(self):
        m = np.array([[1, 2, 3, 4], [5.5, 6.5, 7.5, 8.5], [9, 10, 11, 12], [13.5, 14.5, 15.5, 16.5]])
        self.assertEqual(m[0][0], 1)
        self.assertEqual(m[0][3], 4)
        self.assertEqual(m[1][0], 5.5)
        self.assertEqual(m[1][2], 7.5)
        self.assertEqual(m[2][2], 11)
        self.assertEqual(m[3][0], 13.5)
        self.assertEqual(m[3][2], 15.5)
    
    def test_2x2_matrix(self):
        m = np.array([[-3, 5], [1, -2]])
        self.assertEqual(m[0][0], -3)
        self.assertEqual(m[0][1], 5)
        self.assertEqual(m[1][0], 1)
        self.assertEqual(m[1][1], -2)
    
    def test_3x3_matrix(self):
        m = np.array([[-3, 5, 0], [1, -2, -7], [0, 1, 1]])
        self.assertEqual(m[0][0], -3)
        self.assertEqual(m[1][1], -2)
        self.assertEqual(m[2][2], 1)

    def test_identical_matrix_equality(self):
        a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
        b = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
        self.assertTrue(np.array_equal(a, b))
    
    def test_different_matrix_equality(self):
        a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
        b = np.array([[2, 3, 4, 5], [6, 7, 8, 9], [8, 7, 6, 5], [4, 3, 2, 1]])
        self.assertFalse(np.array_equal(a, b))

    def test_multiply_matrices(self):
        a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
        b = np.array([[-2, 1, 2, 3], [3, 2, 1, -1], [4, 3, 6, 5], [1, 2, 7, 8]])
        product = np.array([[20, 22, 50, 48], [44, 54, 114, 108], [40, 58, 110, 102], [16, 26, 46, 42]])
        self.assertTrue(np.array_equal(a.dot(b), product))

    def test_matrix_tuple_multiply(self):
        a = np.array([[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]])
        b = Tuple(1, 2, 3, 1)
        self.assertEqual(Matrix.multiply_tuple(a, b), Tuple(18, 24, 33, 1))

    def test_matrix_multiply_identity(self):
        a = np.array([[0, 1, 2, 4], [1, 2, 4, 8], [2, 4, 8, 16], [4, 8, 16, 32]])
        self.assertTrue(np.array_equal(a.dot(np.identity(4)), a))

    def test_identity_matrix_multiply_tuple(self):
        a = Tuple(1, 2, 3, 4)
        self.assertEqual(Matrix.multiply_tuple(np.identity(4), a), a)

    def test_transpose_matrix(self):
        a = np.array([[0, 9, 3, 0], [9, 8, 0, 8], [1, 8, 5, 3], [0, 0, 5, 8]])
        a_transposed = np.array([[0, 9, 1, 0], [9, 8, 8, 0], [3, 0, 5, 5], [0, 8, 3, 8]])
        self.assertTrue(np.array_equal(a.transpose(), a_transposed))

    def test_transpose_identity_matrix(self):
        self.assertTrue(np.array_equal(np.identity(4).transpose(), np.identity(4)))

    def test_determinant_2x2_matrix(self):
        a = np.array([[1, 5], [-3, 2]])
        self.assertEqual(Matrix.determinant(a), 17)

    def test_submatrix_3x3(self):
        a = np.array([[1, 5, 0], [-3, 2, 7], [0, 6, -3]])
        submatrix = np.array([[-3, 2], [0, 6]])
        self.assertTrue(np.array_equal(Matrix.submatrix(a, 0, 2), submatrix))

    def test_submatrix_4x4(self):
        a = np.array([[-6, 1, 1, 6], [-8, 5, 8, 6], [-1, 0, 8, 2], [-7, 1, -1, 1]])
        submatrix = np.array([[-6, 1, 6], [-8, 8, 6], [-7, -1, 1]])
        self.assertTrue(np.array_equal(Matrix.submatrix(a, 2, 1), submatrix))

    def test_minor_3x3(self):
        a = np.array([[3, 5, 0], [2, -1, -7], [6, -1, 5]])
        b = Matrix.submatrix(a, 1, 0)
        self.assertAlmostEqual(Matrix.determinant(b), 25, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.minor(a, 1, 0), 25, delta = Constants.epsilon)

    def test_cofactor_3x3(self):
        a = np.array([[3, 5, 0], [2, -1, -7], [6, -1, 5]])
        self.assertAlmostEqual(Matrix.minor(a, 0, 0), -12, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.cofactor(a, 0, 0), -12, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.minor(a, 1, 0), 25, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.cofactor(a, 1, 0), -25, delta = Constants.epsilon)

    def test_determinant_3x3(self):
        a = np.array([[1, 2, 6], [-5, 8, -4], [2, 6, 4]])
        self.assertAlmostEqual(Matrix.cofactor(a, 0, 0), 56, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.cofactor(a, 0, 1), 12, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.cofactor(a, 0, 2), -46, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.determinant(a), -196, delta = Constants.epsilon)
        
    def test_determinant_4x4(self):
        a = np.array([[-2, -8, 3, 5], [-3, 1, 7, 3], [1, 2, -9, 6], [-6, 7, 7, -9]])
        self.assertAlmostEqual(Matrix.cofactor(a, 0, 0), 690, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.cofactor(a, 0, 1), 447, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.cofactor(a, 0, 2), 210, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.cofactor(a, 0, 3), 51, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.determinant(a), -4071, delta = Constants.epsilon)

    def test_invertible_matrix(self):
        a = np.array([[6, 4, 4, 4], [5, 5, 7, 6], [4, -9, 3, -7], [9, 1, 7, -6]])
        self.assertAlmostEqual(Matrix.determinant(a), -2120, delta = Constants.epsilon)
        self.assertTrue(Matrix.invertible(a))

    def test_noninvertible_matrix(self):
        a = np.array([[-4, 2, -2, -3], [9, 6, 2, 6], [0, -5, 1, -5], [0, 0, 0, 0]])
        self.assertAlmostEqual(Matrix.determinant(a), 0, delta = Constants.epsilon)
        self.assertFalse(Matrix.invertible(a))

    def test_inverse_matrix(self):
        a = np.array([[-5, 2, 6, -8], [1, -5, 1, 8], [7, 7, -6, -7], [1, -3, 7, 4]])
        b = Matrix.inverse(a)
        a_inverse = np.array([[0.21805, 0.45113, 0.24060, -0.04511], [-0.80827, -1.45677, -0.44361, 0.52068], [-0.07895, -0.22368, -0.05263, 0.19737], [-0.52256, -0.81391, -0.30075, 0.30639]])
        self.assertAlmostEqual(Matrix.determinant(a), 532, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.cofactor(a, 2, 3), -160, delta = Constants.epsilon)
        self.assertAlmostEqual(b[3][2], -160/532, delta = Constants.epsilon)
        self.assertAlmostEqual(Matrix.cofactor(a, 3, 2), 105, delta = Constants.epsilon)
        self.assertAlmostEqual(b[2][3], 105/532, delta = Constants.epsilon)
        self.assertTrue(np.allclose(a_inverse, b, atol = Constants.epsilon))

    def test_inverse_matrix_1(self):
        a = np.array([[8, -5, 9, 2], [7, 5, 6, 1], [-6, 0, 9, 6], [-3, 0, -9, -4]])
        a_inverse = np.array([[-0.15385, -0.15385, -0.28205, -0.53846], [-0.07692, 0.12308, 0.02564, 0.03077], [0.35897, 0.35897, 0.43590, 0.92308], [-0.69231, -0.69231, -0.76923, -1.92308]])
        self.assertTrue(np.allclose(Matrix.inverse(a), a_inverse, atol = Constants.epsilon))

    def test_inverse_matrix_2(self):
        a = np.array([[9, 3, 0, 9], [-5, -2, -6, -3], [-4, 9, 6, 4], [-7, 6, 6, 2]])
        a_inverse = np.array([[-0.04074, -0.07778, 0.14444, -0.22222], [-0.07778, 0.03333, 0.36667, -0.33333], [-0.02901, -0.14630, -0.10926, 0.12963], [0.17778, 0.06667, -0.26667, 0.33333]])
        self.assertTrue(np.allclose(Matrix.inverse(a), a_inverse, atol = Constants.epsilon))

    def test_product_inverse(self):
        a = np.array([[3, -9, 7, 3], [3, -8, 2, -9], [-4, 4, 4, 1], [-6, 5, -1, 1]])
        b = np.array([[8, 2, 2, 2], [3, -1, 7, 0], [7, 0, 5, 4], [6, -2, 0, -5]])
        c = np.dot(a, b)
        self.assertTrue(np.allclose(np.dot(c, Matrix.inverse(b)), a, atol = Constants.epsilon))

if __name__ == '__main__':
    unittest.main()
