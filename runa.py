import moderngl_window as mglw
import moderngl
import numpy as np
import time
from pyrr import Matrix44

# Create an orthographic projection matrix


WIDTH, HEIGHT = 800,800


class Runa(mglw.WindowConfig):
    resource_dir = "shaders"  # built in prefix, how neat is that??
    window_size = WIDTH, HEIGHT  # same with windows, so convienent
    gl_version = (4, 3)
    title = "N-Body Simulation"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ctx = moderngl.create_context()

        # simulation parameters
        self.n = int(5e4)  # number of bodies
        self.dt = 10
        self.g = 6e-11



        self.compute_shader = self.load_compute_shader("compute_shader.glsl")

        # Initialize particle data (positions, velocities)
        self.particle_data = np.zeros(self.n, dtype=[
            ('position', np.float32, 4),  # xyz = position, w = mass
            ('velocity', np.float32, 4),  # xyz = velocity, w = padding
        ])

        # Random initial positions and velocities
        self.particle_data['position'][:, :2] = np.random.uniform(-1.0, 1.0, (self.n, 2))
        self.particle_data['position'][:, 2] = 0
        self.particle_data['position'][:, 3] = 1.0
        self.particle_data['velocity'][:, :3] = [0, 0, 0]



        # Create buffers
        self.particle_buffer = self.ctx.buffer(self.particle_data.tobytes())
        self.particle_buffer.bind_to_storage_buffer(0)

        self.render_program = self.ctx.program(
            vertex_shader=open(self.resource_dir + '/vertex_shader.glsl').read(),
            fragment_shader=open(self.resource_dir + '/fragment_shader.glsl').read(),
        )

        # Create the vertex array object (VAO) for rendering
        self.vao = self.ctx.vertex_array(
            self.render_program,
            [(self.particle_buffer, '4f', 'in_position')],
        )
        projection = Matrix44.orthogonal_projection(left=-1.0, right=1.0, bottom=-1.0, top=1.0, near=-1.0, far=1.0,
                                                    dtype='f4')
        self.render_program['projection'].write(projection)

    def update_particles(self):
        # Bind the time step and particle count uniforms
        self.compute_shader['dt'].value = self.dt
        self.compute_shader['num_particles'].value = self.n
        self.compute_shader["G"].value = self.g

        # Dispatch the compute shader
        num_workgroups = (self.n + 512) // 512  # 256 is the local size in compute shader
        self.compute_shader.run(num_workgroups, 1, 1)

    def render(self, time: float, frame_time: float):
        self.ctx.viewport = (0, 0, self.window_size[0], self.window_size[1])
        self.ctx.clear(0, 0, 0)

        # Update particle positions using the compute shader
        self.update_particles()

        # Render particles using the vertex array
        self.vao.render(mode=moderngl.POINTS)




if __name__ == '__main__':

    mglw.run_window_config(Runa)