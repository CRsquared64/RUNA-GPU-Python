'''

-----------------
        |
   0    |    1
--------|-------
        |
   2    |     3
-----------------
'''
import math
import numpy as np

def np_to_body(pos, vel, G, dt):
    pos = pos.tolist()
    vel = vel.tolist()
    bodies = []
    for i in range(pos):
        bdy = Body(pos[i][0], pos[i][1])
        bdy.G = G
        bdy.dt = dt
        bdy.xv = (vel[i][0])
        bdy.yv = vel[i][1]
        bodies.append(bdy)
    return bodies

class Body:
    G = 0.6
    dt = 1
    threshold = 3.14

    def __init__(self, x, y, mass=1):
        self.x = x
        self.y = y

        self.xv = 0
        self.yv = 0

        self.fx = 0
        self.fy = 0
        self.radius = 1
        self.mass = mass
        self.ignore = []
        self.depth = None

    def force_calculation(body, obj):
        obj_x = obj.x
        obj_y = obj.y
        obj_dist_x = obj_x - body.x
        obj_dist_y = obj_y - body.y

        dist = math.sqrt(obj_dist_x ** 2 + obj_dist_y ** 2)
        force = (body.G * body.mass * obj.mass) / dist ** 2

        angle = math.atan2(obj_dist_y, obj_dist_x)

        force_x = math.cos(angle) * force
        force_y = math.sin(angle) * force

        return force_x, force_y

    def node_check(self, node):
        s = node.max_x - node.min_x
        distance_x = self.x - node.x
        distance_y = self.y - node.y
        d = math.sqrt(distance_x ** 2 + distance_y ** 2)
        s_d = s / d
        return s_d

    def update_position(self, bodies):
        total_fx = 0
        total_fy = 0

        total_impulse_x = 0
        total_impulse_y = 0
        for body in bodies:
            if body == self or body in self.ignore:
                continue
            fx, fy = self.force_calculation(body)
            if isinstance(body, Body):
                impulse_x, impulse_y = self.collide(body)
                total_impulse_x += impulse_x * body.mass
                total_impulse_y += impulse_y * body.mass

            total_fx += fx
            total_fy += fy

        self.xv += total_fx / self.mass * self.dt
        self.yv += total_fy / self.mass * self.dt

        self.xv -= total_impulse_x
        self.yv -= total_impulse_y

    def final_update(self):
        self.x += self.xv * self.dt
        self.y += self.yv * self.dt

    def eat_me(self, other):
        # Calculate relative position and velocity
        rel_pos_x = other.x - self.x
        rel_pos_y = other.y - self.y
        rel_vel_x = other.xv - self.xv
        rel_vel_y = other.yv - self.yv
        # Calculate the distance between the bodies
        dist = math.sqrt(rel_pos_x ** 2 + rel_pos_y ** 2)
        if dist < 2 * 4:
            self.mass += other.mass
            self.x = (other.x + self.x) // 2
            self.y = (other.y + self.y) // 2

            self.xv += other.xv
            self.yv += other.yv
            self.radius += other.radius

            other.x, other.y = -10000, -10000

    def collide(self, other):
        # Calculate relative position and velocity
        rel_pos_x = other.x - self.x
        rel_pos_y = other.y - self.y
        rel_vel_x = other.xv - self.xv
        rel_vel_y = other.yv - self.yv
        # Calculate the distance between the bodies
        dist = math.sqrt(rel_pos_x ** 2 + rel_pos_y ** 2)

        # Check if the bodies are overlapping
        if dist < 2 * 3.5:
            self.ignore.append(other)
            # Calculate the normal vector
            normal_x = rel_pos_x / dist
            normal_y = rel_pos_y / dist

            # Calculate relative velocity along the normal vector
            vel_along_normal = rel_vel_x * normal_x + rel_vel_y * normal_y

            # Check if the bodies are moving towards each other
            if vel_along_normal < 0:
                # Calculate the impulse scalar
                impulse_scalar = -2 * vel_along_normal / (self.mass + other.mass)

                # Calculate impulse components
                impulse_x = impulse_scalar * normal_x * 1
                impulse_y = impulse_scalar * normal_y * 1

                return impulse_x, impulse_y

        if other in self.ignore and dist > 2 * 10:
            self.ignore.remove(other)
        return 0, 0


'''
    # Update velocities
    self.xv -= impulse_x * other.mass
    self.yv -= impulse_y * other.mass
    other.xv += impulse_x * self.mass
    other.yv += impulse_y * self.mass
'''

'''
self.x += self.xv * self.dt * 0.3
self.y += self.yv * self.dt * 0.3
other.x += other.xv * other.dt * 0.3
other.y += other.yv * other.dt * 0.3
'''


class Node:
    def __init__(self, minx, miny, maxx, maxy, depth=0):
        self.children = [None, None, None, None]
        self.min_x = minx
        self.min_y = miny
        self.max_x = maxx
        self.max_y = maxy

        self.area = Area(self.min_x, self.min_y, self.max_x, self.max_y)
        self.child_area = []
        self.x = 0
        self.y = 0
        self.mass = 0
        self.update_child_area()
        self.depth = depth

    def update_center_mass(self):
        count = 0
        mass = 0
        x = 0
        y = 0
        for child in self.children:
            if child is not None:
                x += child.x
                y += child.y
                mass += child.mass
                count += 1
                child.depth = self.depth
        if count != 0:
            x = x / count
            y = y / count
            self.x = x
            self.y = y
            self.mass = mass

    def update_child_area(self):
        mid_x = (self.min_x + self.max_x) / 2
        mid_y = (self.min_y + self.max_y) / 2
        for i in range(4):
            if i == 0:
                self.child_area.append(Area(self.min_x, mid_y, mid_x, self.max_y))
            elif i == 1:
                self.child_area.append(Area(mid_x, mid_y, self.max_x, self.max_y))
            elif i == 2:
                self.child_area.append(Area(self.min_x, self.min_y, mid_x, mid_y))
            elif i == 3:
                self.child_area.append(Area(mid_x, self.min_y, self.max_x, mid_y))


class Area:
    def __init__(self, minx, miny, maxx, maxy):
        self.min_x = minx
        self.min_y = miny
        self.max_x = maxx
        self.max_y = maxy


class QuadTree:
    def __init__(self, area, max_depth=200):
        self.area = area
        self.root = Node(area.min_x, area.min_y, area.max_x, area.max_y)
        self.max_depth = max_depth

    def check_in_range(self,body):
        if self.area.min_x < body.x <= self.area.max_x:
            if self.area.min_y <= body.y < self.area.max_y:
                return True
        else:
            return False
    def get_quadrant(self, body, area):
        mid_x = (area.min_x + area.max_x) / 2
        mid_y = (area.min_y + area.max_y) / 2
        if body.x < mid_x:
            if body.y < mid_y:
                return 2
            else:
                return 0
        else:
            if body.y < mid_y:
                return 3
            else:
                return 1

    def insert(self, body, node=None, depth=0):
        node = node if node else self.root
        if depth == self.max_depth:
            print(body.x, body.y, node.x, node.y)
            print("Max Depth")
            return
        quadrant = self.get_quadrant(body, Area(node.min_x, node.min_y, node.max_x, node.max_y))
        if isinstance(node.children[quadrant], Body):
            if body.x == node.children[quadrant].x and body.y == node.children[quadrant].y:
                body.x += 5

            # If the quadrant already contains a body, subdivide and reinsert
            bodies = [node.children[quadrant], body]
            node.children[quadrant] = None  # Reset to None before subdivision
            self.subdivide(node, quadrant)
            for b in bodies:
                self.insert(b, node.children[quadrant], depth + 1)
        elif isinstance(node.children[quadrant], Node):
            # If the quadrant contains a node, recursively insert into it
            self.insert(body, node.children[quadrant], depth + 1)
        else:
            # If the quadrant is empty, insert the body directly
            node.children[quadrant] = body

    def subdivide(self, node, quadrant):
        mid_x = (node.min_x + node.max_x) / 2
        mid_y = (node.min_y + node.max_y) / 2
        if quadrant == 0:
            node.children[quadrant] = Node(node.min_x, mid_y, mid_x, node.max_y, node.depth + 1)
        elif quadrant == 1:
            node.children[quadrant] = Node(mid_x, mid_y, node.max_x, node.max_y, node.depth + 1)
        elif quadrant == 2:
            node.children[quadrant] = Node(node.min_x, node.min_y, mid_x, mid_y, node.depth + 1)
        elif quadrant == 3:
            node.children[quadrant] = Node(mid_x, node.min_y, node.max_x, mid_y, node.depth + 1)


if __name__ == "__main__":
    testBody = Body(5, 6, 7)
    testBody2 = Body(8, 9, 10)
    force_x, force_y = testBody.force_calculation(testBody2)
    print(force_x, force_y)
# i thought it wasnt working... turns out im dumb it works fine
# i was like oh its not drawing all nodes, two or more bodies are in the same quadrant.
# but yes that shouldhappen, the only reason they dont look seperated is because im not drawing the final level of boxes
# because there are multiple bodies to one node, im only drawing node to node relations
