import random

import moderngl_window as mglw
import moderngl
import numpy as np
import math
from pyrr import Matrix44

WIDTH, HEIGHT = 800, 800


class Runa(mglw.WindowConfig):
    resource_dir = "shaders"  # built in prefix, how neat is that??
    window_size = WIDTH, HEIGHT  # same with windows, so convienent
    gl_version = (4, 3)
    title = "N-Body Simulation"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ctx = moderngl.create_context()

        # simulation parameters
        self.n = int(250 ** 2)  # number of bodies
        self.dt = 10
        self.g = 6E-11

        self.compute_shader = self.load_compute_shader("compute_shader.glsl")

        self.position_data = np.zeros((self.n, 4), dtype=np.float32)
        self.velocity_data = np.zeros((self.n, 4), dtype=np.float32)

        pos, vel = self.square()  # options are square, circle
        self.position_data[:] = pos
        self.velocity_data[:] = vel

        self.position_buffer = self.ctx.buffer(self.position_data.tobytes())
        self.velocity_buffer = self.ctx.buffer(self.velocity_data.tobytes())

        self.position_buffer.bind_to_storage_buffer(0)
        self.velocity_buffer.bind_to_storage_buffer(1)

        self.render_program = self.ctx.program(
            vertex_shader=open(self.resource_dir + '/vertex_shader.glsl').read(),
            fragment_shader=open(self.resource_dir + '/fragment_shader.glsl').read(),
        )

        self.vao = self.ctx.vertex_array(
            self.render_program,
            [
                (self.position_buffer, '4f', 'in_position'),  # Position attribute
                (self.velocity_buffer, '4f', 'in_velocity')  # Velocity attribute
            ]
        )

        projection = Matrix44.orthogonal_projection(left=-1, right=1, bottom=-1, top=1, near=-1.0, far=1.0,
                                                    dtype='f4')
        self.render_program['projection'].write(projection)
        print("Particle Data Size:", len(self.position_data))

    def update_particles(self):
        self.compute_shader['dt'].value = self.dt
        self.compute_shader['num_particles'].value = self.n
        self.compute_shader["G"].value = self.g

        num_workgroups = (self.n + 512) // 512  #
        self.compute_shader.run(num_workgroups, 1, 1)

    def render(self, time: float, frame_time: float):
        self.ctx.viewport = (0, 0, self.window_size[0], self.window_size[1])
        self.ctx.clear(0, 0, 0)
        self.update_particles()
        self.vao.render(mode=moderngl.POINTS)

    def uniform_square(self):
        r = int(math.sqrt(self.n))
        pos = []

        scale_factor = (2 / (r - 1))

        for i in range(r):
            for j in range(r):
                x = i * scale_factor - 1
                y = j * scale_factor - 1
                z = 0
                mass = 1
                pos.append([x, y, z, mass])

        vel = np.zeros((self.n, 4))
        return np.array(pos), vel

    def random(self):
        pos = []
        vel = []
        for i in range(self.n):
            x = random.uniform(-WIDTH, WIDTH)
            y = random.uniform(-HEIGHT,HEIGHT)
            z = 0
            mass = 1
            xv = 0
            yv = 0
            zv = 0
            padding = 1
            pos.append([x,y,z,mass])
            vel.append([xv,yv,zv,padding])
        return np.array(pos), np.array(vel)


    def square(self):

        pos = np.random.uniform(-1, 1, (self.n, 2))
        z = np.zeros((self.n, 1))
        pos = np.hstack((pos, z))

        mass = np.ones((self.n, 1))
        pos = np.hstack((pos, mass))

        vel = np.zeros((self.n,4))

        return pos, vel

    def circle(self):
        min_dist = 0.025
        pos = [[0, 0, 0, 1000]]
        vel = [[0, 0, 0,0]]
        for i in range(self.n - 1):
            angle = random.random() * math.pi * 2
            distance = (random.random()) * 0.6 + min_dist

            x = math.cos(angle) * distance * 1
            y = math.sin(angle) * distance * 1
            z = 0
            mass = 1

            pos.append([x, y, z, mass])

            xv = math.cos(angle + math.pi / 2) * distance * 0.01
            yv = math.sin(angle + math.pi / 2) * distance * 0.01
            zv = 0

            vel.append([xv, yv, zv,0])
        return np.array(pos), np.array(vel)

    def spiral(self):
        arm_separation = np.pi
        noise_std = 0.1
        a  = 0.1
        b = 0.3
        n_arm_points = self.n // 2  # Points per arm
        theta = np.linspace(0, 4 * np.pi, n_arm_points)  # Angle range for one arm

        # Spiral equation for radius
        r = a + b * theta  # r = a + b * theta

        # First arm
        x1 = r * np.cos(theta)
        y1 = r * np.sin(theta)

        # Second arm (shifted by `arm_separation`)
        x2 = r * np.cos(theta + arm_separation)
        y2 = r * np.sin(theta + arm_separation)

        # Combine both arms
        x = np.concatenate([x1, x2])
        y = np.concatenate([y1, y2])

        x += np.random.normal(0, noise_std, size=x.shape)
        y += np.random.normal(0, noise_std, size=y.shape)
        # Normalize x and y to the range [-1, 1]


        # Create z values (all 0) and mass values (all 1)
        z = np.zeros_like(x)
        mass = np.ones_like(x)

        distance = np.sqrt(x ** 2 + y ** 2)  # Radial distance in 2D
        angle = np.arctan2(y, x)  # Angle in 2D (from x-axis)

        # Compute velocity components (rotated by 90 degrees)
        xv = np.cos(angle + np.pi / 2) * distance * 3
        yv = np.sin(angle + np.pi / 2) * distance * 3
        zv = np.zeros_like(xv)  # Since all motion is in the xy-plane
        p  = np.ones_like(xv)

        vel = np.column_stack([xv,yv,zv,p])

        # Stack the results into a (n_points, 4) array
        galaxy = np.column_stack([x, y, z, mass])
        return galaxy, vel

if __name__ == '__main__':
    mglw.run_window_config(Runa)
