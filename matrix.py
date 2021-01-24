import math
import numpy as np
from constants import Constants
from tuple import Tuple

class Matrix:
    def multiply_tuple(matrix: np.ndarray, tuple: Tuple):
        x = matrix[0][0] * tuple.x + matrix[0][1] * tuple.y + matrix[0][2] * tuple.z + matrix[0][3] * tuple.w
        y = matrix[1][0] * tuple.x + matrix[1][1] * tuple.y + matrix[1][2] * tuple.z + matrix[1][3] * tuple.w
        z = matrix[2][0] * tuple.x + matrix[2][1] * tuple.y + matrix[2][2] * tuple.z + matrix[2][3] * tuple.w
        w = matrix[3][0] * tuple.x + matrix[3][1] * tuple.y + matrix[3][2] * tuple.z + matrix[3][3] * tuple.w
        t = Tuple(x, y, z, w)
        return t

    def determinant(matrix: np.ndarray):
        return np.linalg.det(matrix)
    
    def submatrix(matrix: np.ndarray, row: int, column: int):
        # https://stackoverflow.com/questions/53716797/fastest-way-to-delete-extract-a-submatrix-from-a-numpy-matrix
        return np.delete(np.delete(matrix, row, axis=0), column, axis=1)

    def minor(matrix: np.ndarray, row: int, column: int):
        return np.linalg.det(Matrix.submatrix(matrix, row, column))

    def cofactor(matrix: np.ndarray, row: int, column: int):
        # cofactor is minor negated if row + column is odd
        if (row + column) % 2 is 1:
            return Matrix.minor(matrix, row, column) * -1
        else:
            return Matrix.minor(matrix, row, column)

    def invertible(matrix: np.ndarray):
        if math.isclose(Matrix.determinant(matrix), 0, abs_tol=Constants.epsilon):
            return False
        else:
            return True
            
    def inverse(matrix: np.ndarray) -> np.ndarray:
        return np.linalg.inv(matrix)
    