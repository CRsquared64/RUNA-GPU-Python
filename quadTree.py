import cupy as cp # noqa

class Body:
    G = 0.6
    dt = 1
    THRESH = 0.7
    def __init__(self,x,y,mass=1):
        self.x = cp.array([x])
        self.y = cp.array([y])
        self.mass = mass
        self.xv = cp.array([0.0])
        self.yv = cp.array([0.0])

    def force_calculation(self,obj):
        obj_dist_x = obj.x - self.x
        obj_dist_y = obj.y = self.y

        dist = (obj_dist_x ** 2 + obj_dist_y ** 2) ** 0.5
        force = (self.G * self.mass * obj.mass) / dist ** 2
        angle = cp.arctan2(obj_dist_y, obj_dist_x)

        force_x = cp.cos(angle) * force
        force_y = cp.sin(angle) * force

        return force_x, force_y



