from tuple import *

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
    p = Projectile(Point(0, 1, 0), Vector(1, 1, 0).normalize())
    e = Environment(Vector(0, -0.1, 0), Vector(-0.01, 0, 0))

    while p.position.y >= 0:
        print(f"Position {p.position}")
        p.tick(e)