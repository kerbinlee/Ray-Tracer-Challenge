from typing import Iterable

class Intersection:
    def __init__(self, t: float, object, u: float = None, v: float = None):
        self.t: float = t
        self.object = object
        self.u: float = u
        self.v: float = v
    
    def intersections(*i: Iterable['Intersection']) -> Iterable['Intersection']:
        return i

    def hit(intersections: Iterable['Intersection']) -> 'Intersection':
        hit = None
        for intersection in intersections:
            if intersection.t >= 0:
                if hit is None or intersection.t < hit.t:
                    hit = intersection
        return hit

    def __eq__(self, other):
        return self.t == other.t and self.object == other.object
                