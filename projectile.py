from tuple import *
from canvas import *

class Projectile:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def tick(self, environment):
        self.position = self.position + self.velocity
        self.velocity = self.velocity + environment.gravity + environment.wind
        
class Environment:
    def __init__(self, gravity, wind):
        self.gravity = gravity
        self.wind = wind

if __name__ == '__main__':
    p = Projectile(Point(0, 1, 0), Vector(1, 1.8, 0).normalize() * 11.25)
    e = Environment(Vector(0, -0.1, 0), Vector(-0.01, 0, 0))

    c = Canvas(900, 500)
    while p.position.y >= 0:
        print(f"Position {p.position}")
        p.tick(e)
        c.write_pixel(round(p.position.x), round(c.height - p.position.y), Color(1, 1, 1))

    c.canvas_to_ppm()