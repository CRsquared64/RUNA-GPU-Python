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

    def force_calculation(self, obj):
        obj_dist_x = obj.x - self.x
        obj_dist_y = obj.y - self.y

        dist = cp.sqrt(obj_dist_x ** 2 + obj_dist_y ** 2)
        force = (self.G * self.mass * obj.mass) / dist ** 2
        angle = cp.arctan2(obj_dist_y, obj_dist_x)

        force_x = cp.cos(angle) * force
        force_y = cp.sin(angle) * force

        return force_x, force_y

    def node_check(self, node):
        s = node.max_x - node.min_x
        distance_x = self.x - node.x
        distance_y = self.y - node.y
        d = (distance_x ** 2 + distance_y ** 2) ** 0.5
        s_d = s / d
        return s_d


    def update_position(self, bodies):
        total_fx = cp.array([0.0])
        total_fy = cp.array([0.0])

        total_impulse_x = cp.array([0.0])
        total_impulse_y = cp.array([0.0])
        for body in bodies:
            if body == self:
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

        self.x += self.xv * self.dt
        self.y += self.yv * self.dt

class Node:
    def __init__(self, minx, miny, maxx, maxy, depth=0):
        self.children = [None] * 4  # Use Python list here
        self.min_x = cp.array([minx])
        self.min_y = cp.array([miny])
        self.max_x = cp.array([maxx])
        self.max_y = cp.array([maxy])
        self.area = Area(self.min_x, self.min_y, self.max_x, self.max_y)
        self.child_area = []  # Use Python list
        self.x = cp.array([0])
        self.y = cp.array([0])
        self.mass = 0
        self.update_child_area()
        self.depth = depth


    def update_center_mass(self):
        count = cp.array([0])
        mass = 0
        x = cp.array([0])
        y = cp.array([0])

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
    def __init__(self, minx,miny,maxx,maxy): # check types pls
        self.min_x = cp.array([minx])
        self.min_y = cp.array([miny])
        self.max_x = cp.array([maxx])
        self.max_y = cp.array([maxy])

        print(type(self.min_x))

class QuadTree:
    def __init__(self,area,max_depth=256):
        self.area = area
        self.root = Node(area.min_x,area.min_y,area.max_x,area.max_y)
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
    area = Area(0, 0, 128, 128)
    tree = QuadTree(area)
    tree.insert(Body(10, 70))
    tree.insert(Body(10, 71))
    tree.insert(Body(70, 80))
    tree.insert(Body(70, 81))
    print(tree.root.children[0].children[2].children)
    print(tree.root.children[0].children[2].children[2].min_y)