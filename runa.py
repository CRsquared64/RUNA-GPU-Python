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
        self.n = int(400 ** 2)  # number of bodies
        self.dt = 2
        self.g = 6.67e-10
        self.compute_shader = self.load_compute_shader("compute_shader.glsl")

        self.position_data = np.zeros((self.n, 4), dtype=np.float32)
        self.velocity_data = np.zeros((self.n, 4), dtype=np.float32)

        pos, vel = self.uniform_square()  # options are square, circle
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
            [(self.position_buffer, '4f', 'in_position')]
        )
        projection = Matrix44.orthogonal_projection(left=-4, right=4, bottom=-4, top=4, near=-1.0, far=1.0,
                                                    dtype='f4')
        self.render_program['projection'].write(projection)
        print("Particle Data Size:", len(self.position_data))

    def update_particles(self):
        self.compute_shader['dt'].value = self.dt
        self.compute_shader['num_particles'].value = self.n
        self.compute_shader["G"].value = self.g
        self.compute_shader["min_distance"].value = 0.5
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

        vel = np.zeros((self.n, 4))
        return np.array(pos), vel

    def square(self):

        pos = np.random.uniform(-1.0, 1.0, (self.n, 2))
        z = np.zeros((self.n, 1))
        pos = np.hstack((pos, z))

        mass = np.ones((self.n, 1))
        pos = np.hstack((pos, mass))

        vel = np.zeros((self.n,4))

        return pos, vel

    def rotation_square(self):
        pos = [[0,0,0,10000]]
        vel = [[0,0,0,0]]
        for i in range(self.n - 1):
            x = random.uniform(-0.5,0.5)
            y = random.uniform(-0.5, 0.5)
            z = 0
            mass = 1
            xv = (y-0.1) * 0.003
            yv = -(x-0.1) * 0.003
            zv = 0
            pos.append([x,y,z,mass])
            vel.append([xv,yv,zv,0])
        return np.array(pos), np.array(vel)


    def circle(self):
        min_dist = 0.04
        pos = [[0, 0, 0, 10000]]
        vel = [[0, 0, 0,0]]
        for i in range(self.n - 1):
            angle = random.random() * math.pi * 2
            distance = random.random() + min_dist
            x = math.cos(angle) * distance
            y = math.sin(angle) * distance
            z = 0
            mass = 1

            pos.append([x, y, z, mass])

            xv = math.cos(angle + math.pi / 2) * 0.00001#* distance *0.8
            yv = math.sin(angle + math.pi / 2) * 0.00001 #* distance * 0.8
            zv = 0

            vel.append([xv, yv, zv,0])
        return np.array(pos), np.array(vel)




if __name__ == '__main__':
    mglw.run_window_config(Runa)
