import math

from camera import Camera
from color import Color
from light import PointLight
from material import Material
from sphere import Sphere
from transformations import Transformations
from tuple import Point, Vector
from world import World

if __name__ == '__main__':
    # The floor is an extremely flattened sphere with a matte texture
    floor = Sphere()
    floor.transform = Transformations.scaling(10, 0.1, 10)
    floor.material = Material()
    floor.material.color = Color(1, 0.9, 0.9)
    floor.material.specular = 0

    # The wall on the left has the same scale and color as the floor, but is also rotated and translated into place
    left_wall = Sphere()
    left_wall.transform = Transformations.translation(0, 0, 5)
    left_wall.transform = left_wall.transform.dot(Transformations.rotation_y(-math.pi / 4))
    left_wall.transform = left_wall.transform.dot(Transformations.rotation_x(math.pi / 2))
    left_wall.transform = left_wall.transform.dot(Transformations.scaling(10, 0.1, 10))
    left_wall.material = floor.material

    # The wall on the right is identical to the left wall, but is rotated the opposite direction in y
    right_wall = Sphere()
    right_wall.transform = Transformations.translation(0, 0, 5)
    right_wall.transform = right_wall.transform.dot(Transformations.rotation_y(math.pi / 4))
    right_wall.transform = right_wall.transform.dot(Transformations.rotation_x(math.pi / 2))
    right_wall.transform = right_wall.transform.dot(Transformations.scaling(10, 0.1, 10))
    right_wall.material = floor.material

    # The large sphere in the middle is a unit sphere, translated upward slightly and colored green
    middle = Sphere()
    middle.transform = Transformations.translation(-0.5, 1, 0.5)
    middle_material = Material()
    middle.material.color = Color(0.1, 1, 0.5)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3

    # The smaller green sphere on the right is scaled in half
    right = Sphere()
    right.transform = Transformations.translation(1.5, 0.5, -0.5).dot(Transformations.scaling(0.5, 0.5, 0.5))
    right.material = Material()
    right.material.color = Color(0.5, 1, 0.1)
    right.material.diffuse = 0.7
    right.material.specular = 0.3

    # The smallest sphere is scaled by a third, before being translated
    left = Sphere()
    left.transform = Transformations.translation(-1.5, 0.33, -0.75).dot(Transformations.scaling(0.33, 0.33, 0.33))
    left.material = Material()
    left.material.color = Color(1, 0.8, 0.1)
    left.material.diffuse = 0.7
    left.material.specular = 0.3

    # The light source is white, shining from above and to the left
    world = World()
    world.objects = [floor, left_wall, right_wall, middle, right, left]
    world.light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))

    # Camera
    camera = Camera(100, 50, math.pi / 3)
    camera.transform = World.view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))

    # render the result to a canvas
    canvas = Camera.render(camera, world)
    canvas.canvas_to_ppm()
