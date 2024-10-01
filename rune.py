import random

import moderngl_window as mglw
import moderngl
import numpy as np
import math
from pyrr import Matrix44




class Runa(mglw.WindowConfig):
    resource_dir = "shaders"  # built in prefix, how neat is that??
    window_size = WIDTH, HEIGHT  # same with windows, so convienent
    gl_version = (4, 3)
    title = "N-Body Simulation"

    def __init__(self, pos,vel, **kwargs):
        super().__init__(**kwargs)
        self.ctx = moderngl.create_context()

        # simulation parameters
        self.n = int(300 ** 2)  # number of bodies
        self.dt = 0.01
        self.g = 0.00001

        self.compute_shader = self.load_compute_shader("compute_shader.glsl")

        self.position_data = np.zeros((self.n, 4), dtype=np.float32)
        self.velocity_data = np.zeros((self.n, 4), dtype=np.float32)
 # options are square, circle
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
        projection = Matrix44.orthogonal_projection(left=-1.0, right=1.0, bottom=-1.0, top=1.0, near=-1.0, far=1.0,
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




if __name__ == '__main__':
    mglw.run_window_config(Runa)

