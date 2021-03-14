import math
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
        self.objects: Iterable[Sphere] = []
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

    def shade_hit(world: 'World', comps: Computations, remaining: int = 5) -> Color:
        shadowed = World.is_shadowed(world, comps.over_point)
        surface = PointLight.lighting(comps.object.material, comps.object, world.light, comps.over_point, comps.eyev, comps.normalv, shadowed)
        reflected = World.reflected_color(world, comps, remaining)
        refracted = World.refracted_color(world, comps, remaining)

        material = comps.object.material
        if material.reflective > 0 and material.transparency > 0:
            reflectance = World.schlick(comps)
            return surface + reflected * reflectance + refracted * (1 - reflectance)
        else:
            return surface + reflected + refracted

    def color_at(world: 'World', ray: Ray, remaining: int = 5) -> Color:
        intersections = World.intersect_world(world, ray)
        hit = Intersection.hit(intersections)
        if hit is None:
            return Color(0, 0, 0)
        else:
            comps = Computations.prepare_computations(hit, ray)
            return World.shade_hit(world, comps, remaining)

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

    def reflected_color(world: 'World', comps: Computations, remaining: int = 5) -> Color:
        if remaining <= 0:
            return Color(0, 0, 0)

        if comps.object.material.reflective == 0:
            return Color(0, 0, 0)

        reflect_ray = Ray(comps.over_point, comps.reflectv)
        color = World.color_at(world, reflect_ray, remaining - 1)

        return color * comps.object.material.reflective
        
    def refracted_color(world: 'World', comps: Computations, remaining: int = 5) -> Color:
        if remaining <= 0:
            return Color(0, 0, 0)
        
        if comps.object.material.transparency == 0:
            return Color(0, 0, 0)

        n_ratio = comps.n1 / comps.n2
        cos_i = Vector.dot(comps.eyev, comps.normalv)
        sin2_t = n_ratio ** 2 * (1 - cos_i ** 2)
        if sin2_t > 1:
            return Color(0, 0, 0)

        cos_t = math.sqrt(1.0 - sin2_t)
        direction = comps.normalv * (n_ratio * cos_i - cos_t) - comps.eyev * n_ratio
        refract_ray = Ray(comps.under_point, direction)
        color = World.color_at(world, refract_ray, remaining - 1) * comps.object.material.transparency
        return color
        
    def schlick(comps: Computations) -> float:
        cos = Vector.dot(comps.eyev, comps.normalv)
        if (comps.n1 > comps.n2):
            n = comps.n1 / comps.n2
            sin2_t = n ** 2 * (1.0 - cos ** 2)
            if sin2_t > 1.0:
                return 1.0

            cos_t = math.sqrt(1.0 - sin2_t)
            cos = cos_t

        r0 = ((comps.n1 - comps.n2) / (comps.n1 + comps.n2)) ** 2
        return r0 + (1 - r0) * (1 - cos) ** 5
