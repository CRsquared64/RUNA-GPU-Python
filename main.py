import cupy as cp # noqa
import quadTree
import pygame

pygame.init()
pygame.display.set_caption("Nbody 2")
clock = pygame.time.Clock()

size = 1000
window_x = 800
window_y = 800
screen = pygame.display.set_mode((window_x,window_y))

def force_update(node, body):
    updates = []
    for leaf in node.children:
        if leaf is not None:
            if isinstance(leaf, quadTree.Node):
                if body.node_check(leaf) >= quadTree.Body.threshold:
                    force_update(leaf, body)
                elif body.node_check(leaf) < quadTree.Body.threshold:
                    updates.append(leaf)
            elif isinstance(leaf, quadTree.Body):
                if body == leaf:
                    continue
                updates.append(leaf)

    # Use CuPy arrays for body positions, velocities, and forces
    positions = cp.array([[b.x, b.y] for b in updates])
    masses = cp.array([b.mass for b in updates])

    body_pos = cp.array([body.x, body.y])
    body_mass = body.mass

    # Calculate forces in parallel
    delta_pos = positions - body_pos  # vector differences
    distances = cp.linalg.norm(delta_pos, axis=1)
    forces = (masses * body_mass) / distances ** 2

    # Update body velocity based on forces
    body.xv += cp.sum(forces * (delta_pos[:, 0] / distances))  # x-component of force
    body.yv += cp.sum(forces * (delta_pos[:, 1] / distances))  # y-component of force

    body.update_position()


def click_spawn(bodies):
    x,y, = pygame.mouse.get_pos()
    bodies.append(quadTree.Body(x ,y))
    #bodies[-1].xv = random.uniform(-0.1,0.1)
    #bodies[-1].yv = random.uniform(-0.1, 0.1)
    print(x,y)
    return bodies
def recusrive_search(node, arr,body_arr):
    for leaf in node.children:
        if leaf is not None:
            if isinstance(leaf, quadTree.Node):
                arr.append(leaf)
                recusrive_search(leaf, arr,body_arr)
                leaf.update_center_mass()
            elif isinstance(leaf, quadTree.Body):
                body_arr.append(leaf)

def render_frame(bodies):
    area = quadTree.Area(-window_x, -window_y, window_x, window_y)
    tree = quadTree.QuadTree(area)
    for body in bodies:
        if tree.check_in_range(body):
            tree.insert(body)
        else:
            bodies.remove(body)
    found_bodies = []
    nodes = []
    recusrive_search(tree.root, nodes, found_bodies)

    depths = []
    for body in found_bodies:
        force_update(tree.root, body)
        depths.append(body.depth)
    max_depth = max(depths)
    '''
    for body in found_bodies:
        for other in found_bodies:
            if body == other:
                continue
            body.collide(other)

    for node in nodes:
        ax.add_patch(Rectangle((node.min_x, node.min_y), node.max_x - node.min_x, node.max_y - node.min_y, fill=False))
        for child in node.child_area:
            ax.add_patch(
                Rectangle((child.min_x, child.min_y), child.max_x - child.min_x, child.max_y - child.min_y, fill=False))
                '''
    for body in found_bodies:
        color = (255 / max_depth * body.depth, 255 / max_depth * body.depth, 255 / max_depth * body.depth)
        pygame.draw.circle(screen, (color), (body.x, body.y), body.radius, 1)
    # plt.title(f"Grid Size: {size}")
    # plt.suptitle(f"Barnes-Hut Algorithim Implementation With Quadtrees Where N = {n}")
    del tree
    return bodies

def uniform_bodies(n):
    bodies = []
    for i in range(0,window_x + (window_x // n),(window_x//n + 1)):
        for j in range(0,window_y + 2 * (window_y // n),(window_y//n)):
            bodies.append(quadTree.Body(i,j))
    return bodies


if __name__ == "__main__":
    #odies = generate_filled_circle_bodies(size / 2, size /2, size /6, 512,0.00005)
    #bodies = random_bodies()
    #bodies = uniform_bodies(220)
    #bodies.append(quadTree.Body(size / 2, size / 2, mass=1))
    #bodies = []
    #bodies = uniform_bodies_circle(size/2,size/2,size/16,256)

    #bodies = golden_ratio()
    bodies = uniform_bodies(150)
    print(len(bodies))
    while True:
        screen.fill((10,10, 10))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bodies = click_spawn(bodies)
        bodies = render_frame(bodies)
        pygame.display.update()