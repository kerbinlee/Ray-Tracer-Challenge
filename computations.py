from intersection import Intersection
from ray import Ray
from tuple import *

class Computations(Intersection):
    def __init__(self, t, object):
        super().__init__(t, object)
        self.point: Point = None
        self.eyev: Vector = None
        self.normalv: Vector = None
        self.inside: bool = None
        self.over_point: Point = None

    def prepare_computations(intersection: Intersection, ray: Ray) -> 'Computations':
        comps = Computations(intersection.t, intersection.object)
        comps.point = Ray.position(ray, comps.t)
        comps.eyev = -ray.direction
        comps.normalv = comps.object.normal_at(comps.point)

        if Vector.dot(comps.normalv, comps.eyev) < 0:
            comps.inside = True
            comps.normalv = -comps.normalv
        else:
            comps.inside = False

        comps.over_point = comps.point + comps.normalv * Constants.epsilon

        return comps
