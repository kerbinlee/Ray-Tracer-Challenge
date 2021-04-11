import math
import numpy as np

from canvas import Canvas
from matrix import Matrix
from ray import Ray
from tuple import Point, Vector
from world import World

class Camera:
    def __init__(self, hsize: int, vsize: int, field_of_view: float):
        self.hsize: int = hsize
        self.vsize: int = vsize
        self.field_of_view: float = field_of_view
        self.transform: np.ndarray = np.identity(4)

        half_view = math.tan(self.field_of_view / 2)
        aspect = self.hsize / self.vsize

        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view

        self.pixel_size = (self.half_width * 2) / self.hsize
    
    def ray_for_pixel(camera: 'Camera', px: float, py: float) -> Ray:
        # the offset from the edge of the canvas to the pixel's center
        xoffset = (px + 0.5) * camera.pixel_size
        yoffset = (py + 0.5) * camera.pixel_size

        # the untransformed coordinates of the pixel in world space
        # (remember that the camera looks toward -z, so +x is to the *left*)
        world_x = camera.half_width - xoffset
        world_y = camera.half_height - yoffset

        # using the camera matrix, transform the canvas point and the origin
        # and then compute the ray's direction vector.
        # (remember that the canvas is at z=-1)
        pixel = Matrix.multiply_tuple(Matrix.inverse(camera.transform), Point(world_x, world_y, -1))
        origin = Matrix.multiply_tuple(Matrix.inverse(camera.transform), Point(0, 0, 0))
        direction = Vector.normalize(pixel - origin)

        return Ray(origin, direction)

    def render(camera: 'Camera', world: World) -> Canvas:
        image = Canvas(camera.hsize, camera.vsize)

        for y in range(camera.vsize):
            for x in range(camera.hsize):
                ray = Camera.ray_for_pixel(camera, x, y)
                color = World.color_at(world, ray)
                Canvas.write_pixel(image, x, y, color)

        return image
