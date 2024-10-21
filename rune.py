import os
import sys

import cv2
import moderngl
import moderngl_window as mglw
import numpy as np
from pyrr import Matrix44

WIDTH, HEIGHT = 1920, 1080


class Runa(mglw.WindowConfig):
    resource_dir = "shaders"  # built in prefix, how neat is that??
    window_size = WIDTH, HEIGHT  # same with windows, so convienent
    gl_version = (4, 3)
    title = "N-Body Simulation"

    def __init__(self, pos, vel, g, n, dt, rendered=False, max_frame_time=0, **kwargs):
        super().__init__(**kwargs)
        self.ctx = moderngl.create_context()

        # simulation parameters
        self.n = n  # number of bodies
        self.dt = dt
        self.g = g

        self.render_factor_w = 2  # aspect ratio simplified
        self.render_factor_h = 9 / 8

        self.rendered = rendered

        self.compute_shader = self.load_compute_shader("soft_compute_shader.glsl")

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
            [
                (self.position_buffer, '4f', 'in_position'),  # Position attribute
                (self.velocity_buffer, '4f', 'in_velocity')  # Velocity attribute
            ]
        )

        projection = Matrix44.orthogonal_projection(left=-self.render_factor_w, right=self.render_factor_w,
                                                    bottom=-self.render_factor_h, top=self.render_factor_h, near=-1.0,
                                                    far=1.0,
                                                    dtype='f4')
        self.render_program['projection'].write(projection)
        print("Particle Data Size:", len(self.position_data))

        self.cache_dir = "cache"
        os.makedirs(self.cache_dir, exist_ok=True)  # Create cache dir if it doesn't exist
        if rendered:
            self.frame_count = 0  # To track frame numbers

            # Track time to close after 30 seconds
            self.total_time = 0
            self.max_time = max_frame_time  # seconds

        else:
            pass

    def update_particles(self):
        self.compute_shader['dt'].value = self.dt
        self.compute_shader['num_particles'].value = self.n
        self.compute_shader["G"].value = self.g

        num_workgroups = (self.n + 512) // 512  #
        self.compute_shader.run(num_workgroups, 1, 1)

    def realtime_render(self, time: float, frame_time: float):
        """
        renders in realtime

        """
        self.ctx.viewport = (0, 0, self.window_size[0], self.window_size[1])
        self.ctx.clear(0, 0, 0)
        self.update_particles()
        self.vao.render(mode=moderngl.POINTS)

    def render_to_png(self, time: float, frame_time: float):
        self.total_time += frame_time
        if self.total_time >= self.max_time:
            print("30 seconds passed. Closing application.")
            self.close()
            return

        self.ctx.viewport = (0, 0, self.window_size[0], self.window_size[1])
        self.ctx.clear(0, 0, 0)
        self.update_particles()
        self.vao.render(mode=moderngl.POINTS)

        # Capture frame and save as PNG in cache directory
        frame = self.ctx.screen.read(components=3)  # Read RGB pixels
        frame = np.frombuffer(frame, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV

        # Save frame as PNG
        frame_filename = os.path.join(self.cache_dir, f"frame_{self.frame_count:05d}.jpg")
        cv2.imwrite(frame_filename, frame)
        self.frame_count += 1

    def png_to_vid(self):
        print("Creating video from PNG frames (lossless)...")

        video_filename = "nbody_simulation.avi"
        fourcc = cv2.VideoWriter_fourcc(*'FFV1')  #
        video = cv2.VideoWriter(video_filename, fourcc, 30.0, (WIDTH, HEIGHT))

        # Read all frame files and write them to the video
        for i in range(self.frame_count):
            frame_filename = os.path.join(self.cache_dir, f"frame_{i:05d}.jpg")
            frame = cv2.imread(frame_filename)
            video.write(frame)

        video.release()  # Finalize and save the video
        print(f"Lossless video saved as {video_filename}")

        super().close()

        sys.exit()

    def render(self, time: float, frame_time: float):
        """
        MGLW looks for a function called render to be ran to hence render the simulation, so we have one render function
        which calls upon either realtime or rendered render to render the render. render.
        """
        if self.rendered:
            self.render_to_png(time, frame_time)
        else:
            self.realtime_render(time, frame_time)


if __name__ == '__main__':
    mglw.run_window_config(Runa)
