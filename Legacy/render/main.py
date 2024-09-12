import cupy as cp  # noqa
import quadTree
import pygame

pygame.init()
pygame.display.set_caption("Nbody 2")
clock = pygame.time.Clock()

size = 1000
window_x = 800
window_y = 800
screen = pygame.display.set_mode((window_x, window_y))

# Set up font for FPS display
font = pygame.font.Font(None, 36)  # None uses the default font, 36 is the font size
def prepare_data_for_gpu(bodies):
    # Collect all positions and masses in batches
    positions = cp.array([[body.x[0], body.y[0]] for body in bodies], dtype=cp.float64)
    masses = cp.array([body.mass for body in bodies], dtype=cp.float64)
    return positions, masses


def force_update(node, body, positions, masses):
    updates = []
    for leaf in node.children:
        if leaf is not None:
            if isinstance(leaf, quadTree.Node):
                if body.node_check(leaf) >= quadTree.Body.THRESH:
                    force_update(leaf, body, positions, masses)
                else:
                    updates.append(leaf)
            elif isinstance(leaf, quadTree.Body):
                if body != leaf:
                    updates.append(leaf)

    if not updates:
        return

    # Prepare GPU arrays for updates
    update_positions = cp.array([[b.x[0], b.y[0]] for b in updates], dtype=cp.float64)
    update_masses = cp.array([b.mass for b in updates], dtype=cp.float64)

    body_pos = cp.array([body.x[0], body.y[0]], dtype=cp.float64)
    body_mass = cp.array(body.mass, dtype=cp.float64)

    delta_pos = update_positions - body_pos
    distances = cp.linalg.norm(delta_pos, axis=1)
    distances = cp.where(distances == 0, cp.finfo(cp.float64).eps, distances)
    forces = (update_masses * body_mass) / distances ** 2

    force_x = cp.sum(forces * (delta_pos[:, 0] / distances))
    force_y = cp.sum(forces * (delta_pos[:, 1] / distances))

    body.xv += force_x
    body.yv += force_y

    body.x += body.xv * body.dt
    body.y += body.yv * body.dt


def click_spawn(bodies):
    x, y = pygame.mouse.get_pos()
    bodies.append(quadTree.Body(x, y))
    print(x, y)
    return bodies


def recusrive_search(node, arr, body_arr):
    for leaf in node.children:
        if leaf is not None:
            if isinstance(leaf, quadTree.Node):
                arr.append(leaf)
                recusrive_search(leaf, arr, body_arr)
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

    depths = [body.depth for body in found_bodies]
    if depths:
        max_depth = max(depths)
        for body in found_bodies:
            color_value = int(255 / max_depth * body.depth)
            color = (color_value, color_value, color_value)
            pygame.draw.circle(screen, color, (int(body.x[0]), int(body.y[0])), body.radius, 1)

    del tree
    return bodies


def uniform_bodies(n):
    bodies = []
    for i in range(0, window_x + (window_x // n), (window_x // n + 1)):
        for j in range(0, window_y + 2 * (window_y // n), (window_y // n)):
            bodies.append(quadTree.Body(i, j))
    return bodies


if __name__ == "__main__":
    bodies = uniform_bodies(10)
    print(len(bodies))
    while True:
        screen.fill((10, 10, 10))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bodies = click_spawn(bodies)

        bodies = render_frame(bodies)

        # Display the FPS counter
        fps = int(clock.get_fps())  # Get the current FPS
        fps_text = font.render(f"FPS: {fps}", True, pygame.Color('white'))  # Create the text surface
        screen.blit(fps_text, (10, 10))  # Render the text at the top-left corner

        pygame.display.update()
        clock.tick(60)  # Limit the frame rate to 60 FPS
