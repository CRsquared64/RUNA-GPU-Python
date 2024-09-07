import math
import os

import quadTree
import random
import pygame
from tqdm import tqdm

pygame.init()
pygame.display.set_caption("Nbody 2")
clock = pygame.time.Clock()

size = 1000
window_x = 800
window_y = 800
screen = pygame.display.set_mode((window_x,window_y))

rendered = False
frames = 500

def golden_ratio():
    sped_factor = 0.07
    steps = 5000
    step_size = 1
    bodies = []
    center_y = window_y // 2
    center_x = window_x // 2
    scale = 0.3
    bodies.append(quadTree.Body(center_x,center_y,mass=10000))
    for i in range(50,steps,step_size):
        y = window_y // 2 - int(i * math.sin(i)) * scale
        x = window_x // 2 - int(i * math.cos(i)) * scale
        body = quadTree.Body(x,y)
        #AB = OB - OA
        AB_Y = center_x - x
        AB_x = center_y - y
        AB_Y *= -1
        body.yv = AB_Y * sped_factor
        body.xv = AB_x * sped_factor
        bodies.append(body)
    return bodies


def random_bodies():
    n = 10
    bodies = [quadTree.Body(random.randint(1,window_x),random.randint(1,1080)) for _ in range(n)]
    b_hole = quadTree.Body(size / 2, size / 2,mass=10)
    return bodies

def random_bodies_rotate():
    n = 256
    bodies = [quadTree.Body(random.randint(1,size),random.randint(1,size)) for _ in range(n)]
    for body in bodies:
        body.dt = 0.1
        body.xv = random.uniform(-0.1,0.1)
        body.yv = random.uniform(-0.1,0.1)
    return bodies

def uniform_bodies(n):
    bodies = []
    for i in range(0,window_x + (window_x // n),(window_x//n + 1)):
        for j in range(0,window_y + 2 * (window_y // n),(window_y//n)):
            bodies.append(quadTree.Body(i,j))
    return bodies



def moon_system():
    planet = quadTree.Body(size / 2, size / 2, mass=81)
    moon = quadTree.Body(size / 4, size /2)
    moon.yv = 0.4
    moon.dt = 10
    planet.dt =10
    moon.xv = 0.1
    return [planet,moon]

def three_body():
    return [quadTree.Body(size / 2, size / 3), quadTree.Body(size /2, size / 2), quadTree.Body(size / 2, 2 * size / 3)]


def uniform_bodies_circle(center_x, center_y, radius, n):
    """
    Generate bodies uniformly within the area of a circle with equal spacing between each body.

    Args:
        center_x (float): X coordinate of the center of the circle.
        center_y (float): Y coordinate of the center of the circle.
        radius (float): Radius of the circle.
        n (int): Number of bodies to generate.

    Returns:
        list: List of Body objects.
    """
    bodies = []

    # Calculate the angular spacing between each body
    delta_theta = 2 * math.pi / n

    # Generate bodies
    for i in range(n):
        # Calculate the angle for this body
        theta = i * delta_theta

        # Calculate the position of the body using polar coordinates
        x = center_x + radius * math.cos(theta)
        y = center_y + radius * math.sin(theta)

        bodies.append(quadTree.Body(x, y))

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

def force_update(node, body):
    updates = []
    for leaf in node.children:
        if leaf is not None:
            if isinstance(leaf, quadTree.Node):
                if body.node_check(leaf) >= quadTree.Body.threshold: # < --- should update at once numnubts
                    force_update(leaf,body)
                elif body.node_check(leaf) < quadTree.Body.threshold:
                    updates.append(leaf)
            elif isinstance(leaf, quadTree.Body):
                if body == leaf:
                    continue
                updates.append(leaf)
    body.update_position(updates)

def position_calculation_n_save_stuff(bodies, i):
    i += 1
    area = quadTree.Area(0, 0, size, size)
    tree = quadTree.QuadTree(area)
    for body in bodies:
        tree.insert(body)
    found_bodies = []
    nodes = []
    recusrive_search(tree.root, nodes, found_bodies)
    for body in found_bodies:
        force_update(tree.root, body)
    with open(f"positions/bodies{i}.txt", "w+") as file:
        for body in bodies:
            file.write((f"{body.x}, {body.y}\n"))
    file.close()
    del tree
    return bodies

def render_from_dir(dir):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pygame.quit()
    for file in os.listdir("positions"):
        screen.fill((0,0,0))
        with open(f"positions/{os.fsdecode(file)}", "r") as filehandle:
            lines = filehandle.readlines()
            for line in lines:
                format_line = line.split(",")
                x = float(format_line[0])
                y = float(format_line[1])
                pygame.draw.circle(screen, (255,255,255), (x,y),1,1)
    pygame.display.update()
    clock.tick(60)

def click_spawn(bodies):
    x,y, = pygame.mouse.get_pos()
    bodies.append(quadTree.Body(x ,y))
    #bodies[-1].xv = random.uniform(-0.1,0.1)
    #bodies[-1].yv = random.uniform(-0.1, 0.1)
    print(x,y)
    return bodies


def render_frame(bodies):
    area = quadTree.Area(-window_x , -window_y , window_x  , window_y)
    tree = quadTree.QuadTree(area)
    for body in bodies:
        if tree.check_in_range(body):
            tree.insert(body)
        else:
            bodies.remove(body)
    found_bodies = []
    nodes = []
    recusrive_search(tree.root,nodes, found_bodies)

    depths = []
    for body in found_bodies:
        force_update(tree.root, body)
        depths.append(body.depth)
    max_depth = max(depths)
    for body in found_bodies:
        body.final_update()
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
        color = (255 / max_depth * body.depth,255 / max_depth * body.depth,255 / max_depth * body.depth)
        pygame.draw.circle(screen, (color), (body.x ,body.y ),body.radius,1)
    #plt.title(f"Grid Size: {size}")
    #plt.suptitle(f"Barnes-Hut Algorithim Implementation With Quadtrees Where N = {n}")
    del tree
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

    if not rendered:
        while True:
            screen.fill((10,10, 10))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    bodies = click_spawn(bodies)
            bodies = render_frame(bodies)
            pygame.display.update()
            clock.tick(120)
        # Create the animation
    else:
        with tqdm(total=frames) as pbar:
            for i in range(frames):
                bodies = position_calculation_n_save_stuff(bodies, i)
                pbar.update(1)
        print("Rendering")
        render_from_dir("positions")


