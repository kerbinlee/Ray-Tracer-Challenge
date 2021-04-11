from camera import Camera
from color import Color
from light import PointLight
from obj_file import ObjFile
from tuple import *
from world import World

if __name__ == '__main__':
    parser = ObjFile.parse_obj_file("teapot-low.obj")
    teapot = ObjFile.obj_to_group(parser)
    teapot.material.ambient = .3
    teapot.material.color = Color(.75, .1, .1)

    # The light source is white, shining from above and to the left
    world = World()
    world.objects = [teapot]
    world.light = PointLight(Point(-5, 30, 25), Color(1, 1, 1))

    # Camera
    # camera = Camera(200, 150, math.pi / 3)
    camera = Camera(50, 50, math.pi / 3)
    camera.transform = World.view_transform(Point(0, 30, 25), Point(0, 0, 0), Vector(0, 0, 1))

    # render the result to a canvas
    canvas = Camera.render(camera, world)
    canvas.canvas_to_ppm()
    