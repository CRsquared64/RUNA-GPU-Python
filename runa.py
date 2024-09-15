import random

import moderngl_window as mglw
import moderngl
import numpy as np
import math
from pyrr import Matrix44

WIDTH, HEIGHT = 1080, 1080


class Runa(mglw.WindowConfig):
    resource_dir = "shaders"  # built in prefix, how neat is that??
    window_size = WIDTH, HEIGHT  # same with windows, so convienent
    gl_version = (4, 3)
    title = "N-Body Simulation"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ctx = moderngl.create_context()

        # simulation parameters
        self.n = int(50**2)  # number of bodies
        self.dt = 0.01
        self.g = 0.00001

        self.compute_shader = self.load_compute_shader("compute_shader.glsl")

        # Initialize particle data (positions, velocities)
        self.particle_data = np.zeros(self.n, dtype=[
            ('position', np.float32, 4),  # xyz = position, w = mass
            ('velocity', np.float32, 4),  # xyz = velocity, w = padding
        ])

        pos, vel = self.uniform_square() # options are square, circle
        self.particle_data['position'][:, :4] = pos
        self.particle_data['velocity'][:, :3] = vel

        # Create buffers
        self.particle_buffer = self.ctx.buffer(self.particle_data.tobytes())
        self.particle_buffer.bind_to_storage_buffer(0)

        self.render_program = self.ctx.program(
            vertex_shader=open(self.resource_dir + '/vertex_shader.glsl').read(),
            fragment_shader=open(self.resource_dir + '/fragment_shader.glsl').read(),
        )

        self.vao = self.ctx.vertex_array(
            self.render_program,
            [(self.particle_buffer, '4f', 'in_position')],
        )
        projection = Matrix44.orthogonal_projection(left=-1.0, right=1.0, bottom=-1.0, top=1.0, near=-1.0, far=1.0,
                                                    dtype='f4')
        self.render_program['projection'].write(projection)
        print("Particle Data Size:", len(self.particle_data))

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

        scale_factor = 2 / (r - 1)

        for i in range(r):
            for j in range(r):
                x = i * scale_factor - 1
                y = j * scale_factor - 1
                z = 0
                mass = 1
                pos.append([x, y, z, mass])

        vel = np.zeros((self.n, 3))
        return np.array(pos), vel
    def square(self):

        pos = np.random.uniform(-1.0, 1.0, (self.n, 2))
        z = np.zeros((self.n,1))
        pos = np.hstack((pos, z))

        mass = np.ones((self.n, 1))
        pos = np.hstack((pos, mass))

        vel = [0, 0, 0]

        return pos, vel

    def circle(self):
        min_dist =  0.05
        pos = [[0,0,0,10000]]
        vel = [[0,0,0]]
        for i in range(self.n - 1):
            angle = random.random() * math.pi * 2
            distance = random.random() + min_dist

            x = math.cos(angle) * distance
            y = math.sin(angle) * distance
            z = 0
            mass = 1

            pos.append([x, y, z, mass])

            xv = math.cos(angle + math.pi / 2) * distance / 10000
            yv = math.sin(angle + math.pi / 2) * distance / 10000
            zv = 0

            vel.append([xv, yv, zv])
        return np.array(pos), np.array(vel)




if __name__ == '__main__':
    mglw.run_window_config(Runa)
