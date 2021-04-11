from intersection import Intersection
from ray import Ray
from shape import Shape
from tuple import *
from typing import Iterable

class Computations(Intersection):
    def __init__(self, t, object):
        super().__init__(t, object)
        self.point: Point = None
        self.eyev: Vector = None
        self.normalv: Vector = None
        self.inside: bool = None
        self.over_point: Point = None
        self.under_point: Point = None
        self.reflectv = None
        self.n1: float = None
        self.n2: float = None

    def prepare_computations(intersection: Intersection, ray: Ray, xs: Iterable[Intersection] = None) -> 'Computations':
        comps = Computations(intersection.t, intersection.object)
        comps.point = Ray.position(ray, comps.t)
        comps.eyev = -ray.direction
        comps.normalv = comps.object.normal_at(comps.point, intersection)

        if Vector.dot(comps.normalv, comps.eyev) < 0:
            comps.inside = True
            comps.normalv = -comps.normalv
        else:
            comps.inside = False

        comps.reflectv = Vector.reflect(ray.direction, comps.normalv)

        comps.over_point = comps.point + comps.normalv * Constants.epsilon
        comps.under_point = comps.point - comps.normalv * Constants.epsilon

        # default parameter
        if xs is None:
            xs = [intersection]
        
        containers: Iterable[Shape] = []
        for i in xs:
            if i == intersection:
                if len(containers) == 0:
                    comps.n1 = 1.0
                else:
                    comps.n1 = containers[-1].material.refractive_index
            
            if i.object in containers:
                containers.remove(i.object)
            else:
                containers.append(i.object)
            
            # if i == hit:
            if i == intersection:
                if len(containers) == 0:
                    comps.n2 = 1.0
                else:
                    comps.n2 = containers[-1].material.refractive_index

                break
            
        return comps
