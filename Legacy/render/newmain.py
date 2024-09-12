import cupy as cp
import numpy as np
import pygame
from quadTree import Body

pygame.init()
pygame.display.set_caption("Nbody 2")
clock = pygame.time.Clock()

size = 1000
window_x = 800
window_y = 800
screen = pygame.display.set_mode((window_x, window_y))

font = pygame.font.Font(None, 36)  # Font for FPS display

def batch_process_bodies(bodies):
    num_bodies = len(bodies)

    # Collect data from bodies
    positions = np.array([(body.x.get()[0], body.y.get()[0]) for body in bodies], dtype=np.float64)
    velocities = np.array([(body.xv.get()[0], body.yv.get()[0]) for body in bodies], dtype=np.float64)
    masses = np.array([body.mass for body in bodies], dtype=np.float64)

    # Transfer data to GPU
    positions_gpu = cp.array(positions)
    velocities_gpu = cp.array(velocities)
    masses_gpu = cp.array(masses)

    # Allocate space for forces
    forces_x_gpu = cp.zeros(num_bodies, dtype=cp.float64)
    forces_y_gpu = cp.zeros(num_bodies, dtype=cp.float64)

    # Calculate forces in a more efficient manner
    for i in range(num_bodies):
        dist_x = positions_gpu[:, 0] - positions_gpu[i, 0]
        dist_y = positions_gpu[:, 1] - positions_gpu[i, 1]
        dist_sq = dist_x ** 2 + dist_y ** 2
        dist_sq[dist_sq == 0] = 1  # Avoid division by zero

        force_magnitude = (Body.G * masses_gpu[i] * masses_gpu) / dist_sq
        force_x = (force_magnitude * dist_x) / cp.sqrt(dist_sq)
        force_y = (force_magnitude * dist_y) / cp.sqrt(dist_sq)

        forces_x_gpu[i] = cp.sum(force_x) - force_x[i]
        forces_y_gpu[i] = cp.sum(force_y) - force_y[i]

    # Update velocities and positions
    accelerations_x_gpu = forces_x_gpu / masses_gpu
    accelerations_y_gpu = forces_y_gpu / masses_gpu

    new_velocities_gpu = velocities_gpu + cp.array([accelerations_x_gpu, accelerations_y_gpu]).T * Body.dt
    new_positions_gpu = positions_gpu + new_velocities_gpu * Body.dt

    # Transfer results back to CPU
    new_positions = cp.asnumpy(new_positions_gpu)
    new_velocities = cp.asnumpy(new_velocities_gpu)

    # Update the bodies with new data
    for i, body in enumerate(bodies):
        body.x = cp.array([new_positions[i, 0]], dtype=cp.float64)
        body.y = cp.array([new_positions[i, 1]], dtype=cp.float64)
        body.xv = cp.array([new_velocities[i, 0]], dtype=cp.float64)
        body.yv = cp.array([new_velocities[i, 1]], dtype=cp.float64)

def uniform_bodies(n):
    bodies = []
    step_x = window_x // n + 1
    step_y = window_y // n
    for i in range(0, window_x + step_x, step_x):
        for j in range(0, window_y + 2 * step_y, step_y):
            bodies.append(Body(i, j))
    return bodies

def render_bodies(bodies):
    depths = [body.depth for body in bodies]
    if depths:
        max_depth = max(depths)
        for body in bodies:
            color_value = int(255 / max_depth * body.depth)
            color = (color_value, color_value, color_value)
            pygame.draw.circle(screen, color, (int(body.x.get()[0]), int(body.y.get()[0])), body.radius, 1)

if __name__ == "__main__":
    bodies = uniform_bodies(100)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((10, 10, 10))

        # Measure time to identify bottlenecks
        start_time = pygame.time.get_ticks()

        batch_process_bodies(bodies)
        render_bodies(bodies)

        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, pygame.Color('white'))
        screen.blit(fps_text, (10, 10))

        pygame.display.update()
        clock.tick(60)  # Limit frame rate to 60 FPS

        end_time = pygame.time.get_ticks()
        frame_time = end_time - start_time  # Print time taken for each frame

    pygame.quit()
