import numpy as np

from computations import Computations
from color import Color
from intersection import Intersection
from light import PointLight
from ray import Ray
from sphere import Sphere
from transformations import Transformations
from tuple import Point, Vector
from typing import Iterable

class World:
    def __init__(self):
        self.objects: list[Sphere] = []
        self.light: PointLight = None

    def default_world():
        world = World()
        world.light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
        s1 = Sphere()
        s1.material.color = Color(0.8, 1.0, 0.6)
        s1.material.diffuse = 0.7
        s1.material.specular = 0.2

        s2 = Sphere()
        s2.transform = Transformations.scaling(0.5, 0.5, 0.5)

        world.objects.extend([s1, s2])

        return world

    def intersect_world(world: 'World', ray: Ray) -> Iterable[Intersection]:
        intersections: Iterable[Intersection] = []
        for object in world.objects:
            object_intersections = object.intersect(ray)
            intersections.extend(object_intersections)

        return sorted(intersections, key = lambda intersection: intersection.t)

    def shade_hit(world: 'World', comps: Computations) -> Color:
        shadowed = World.is_shadowed(world, comps.over_point)
        return PointLight.lighting(comps.object.material, world.light, comps.point, comps.eyev, comps.normalv, shadowed)

    def color_at(world: 'World', ray: Ray) -> Color:
        intersections = World.intersect_world(world, ray)
        hit = Intersection.hit(intersections)
        if hit is None:
            return Color(0, 0, 0)
        else:
            comps = Computations.prepare_computations(hit, ray)
            return World.shade_hit(world, comps)

    def view_transform(from_point: Point, to_point: Point, up: Vector) -> np.ndarray:
        forwardv = Point.normalize(to_point - from_point)
        leftv = Vector.cross(forwardv, Vector.normalize(up))
        true_upv = Vector.cross(leftv, forwardv)
        orientation = np.array([[leftv.x, leftv.y, leftv.z, 0], [true_upv.x, true_upv.y, true_upv.z, 0], [-forwardv.x, -forwardv.y, -forwardv.z, 0], [0, 0, 0, 1]])
        return orientation.dot(Transformations.translation(-from_point.x, -from_point.y, -from_point.z))
    
    def is_shadowed(world: 'World', point: Point) -> bool:
        v = world.light.position - point
        distance = v.magnitude()
        direction = Vector.normalize(v)

        r = Ray(point, direction)
        intersections = World.intersect_world(world, r)

        h = Intersection.hit(intersections)
        if h is not None and h.t < distance:
            return True
        else:
            return False
