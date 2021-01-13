from intersection import Intersection
from ray import Ray
from sphere import Sphere
from tuple import *

class Computations(Intersection):
    def __init__(self, t, object):
        super().__init__(t, object)
        self.point: Point = None
        self.eyev: Vector = None
        self.normalv: Vector = None
        self.inside: bool = None

    def prepare_computations(intersection: Intersection, ray: Ray) -> 'Computations':
        comps = Computations(intersection.t, intersection.object)
        comps.point = Ray.position(ray, comps.t)
        comps.eyev = -ray.direction
        comps.normalv = Sphere.normal_at(comps.object, comps.point)

        if Vector.dot(comps.normalv, comps.eyev) < 0:
            comps.inside = True
            comps.normalv = -comps.normalv
        else:
            comps.inside = False

        return comps
