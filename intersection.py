from typing import Iterable

class Intersection:
    def __init__(self, t, object):
        self.t = t
        self.object = object
    
    def intersections(*i: Iterable['Intersection']) -> Iterable['Intersection']:
        return i

    def hit(intersections: Iterable['Intersection']) -> 'Intersection':
        hit = None
        for intersection in intersections:
            if intersection.t >= 0:
                if hit is None or intersection.t < hit.t:
                    hit = intersection
        return hit
            