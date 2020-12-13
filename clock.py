from canvas import Canvas
from tuple import Point
from transformations import Transformations
from matrix import Matrix
from color import Color
import math

class Clock:

    if __name__ == '__main__':
        canvas_size = 300
        canvas = Canvas(canvas_size, canvas_size)
        color = Color(1, 1, 1)
        radius = canvas_size * 3 / 8
        scale = Transformations.scaling(radius, radius, 0)
        origin = Point(0, 0, 0)
        center_translation = Transformations.translation(canvas_size / 2, canvas_size / 2, 0)
        center = Matrix.multiply_tuple(center_translation, origin)

        hour = Point(0, 1, 0) # twelve
        for _ in range(12):
            scaled_hour = Matrix.multiply_tuple(scale, hour)
            positioned_hour = scaled_hour + center
            canvas.write_pixel(round(positioned_hour.x), round(canvas.height - positioned_hour.y), color)
            hour_rotation = Transformations.rotation_z(math.pi / 6)
            hour = Matrix.multiply_tuple(hour_rotation, hour)

        canvas.canvas_to_ppm()
