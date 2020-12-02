import math
import numpy as np

class Transformations:
    def translation(x, y, z):
        m = np.identity(4)
        m[0][3] = x
        m[1][3] = y
        m[2][3] = z
        return m

    def scaling(x, y, z):
        m = np.identity(4)
        m[0][0] = x
        m[1][1] = y
        m[2][2] = z
        return m
    
    def rotation_x(radians):
        m = np.identity(4)
        m[1][1] = math.cos(radians)
        m[1][2] = -math.sin(radians)
        m[2][1] = math.sin(radians)
        m[2][2] = m[1][1]
        return m

    def rotation_y(radians):
        m = np.identity(4)
        m[0][0] = math.cos(radians)
        m[0][2] = math.sin(radians)
        m[2][0] = -math.sin(radians)
        m[2][2] = m[0][0]
        return m

    def rotation_z(radians):
        m = np.identity(4)
        m[0][0] = math.cos(radians)
        m[0][1] = -math.sin(radians)
        m[1][0] = math.sin(radians)
        m[1][1] = m[0][0]
        return m

    def shearing(x_y, x_z, y_x, y_z, z_x, z_y):
        m = np.identity(4)
        m[0][1] = x_y
        m[0][2] = x_z
        m[1][0] = y_x
        m[1][2] = y_z
        m[2][0] = z_x
        m[2][1] = z_y
        return m
