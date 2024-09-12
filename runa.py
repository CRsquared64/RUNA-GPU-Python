import moderngl_window as mglw
from moderngl_window.geometry import quad_fs
import time

WIDTH, HEIGHT = 1920, 1080
k = 0.001


class Runa(mglw.WindowConfig):
    resource_dir = "shaders"  # built in prefix, how neat is that??
    window_size = WIDTH, HEIGHT

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = quad_fs() # basically a screen
        self.prog = self.load_program(vertex_shader='vertex_shader.glsl',
                                      fragment_shader='fragment_shader.glsl')

        self.set_uniform('res', self.window_size)
        self.set_uniform("k", k)
    def set_uniform(self, name, value):
        try:
            self.prog[name] = value
        except KeyError:
            print(f"{name} - not in shader")
    def render(self, time: float, frame_time: float):
        self.set_uniform("time", time)
        self.ctx.clear()
        self.quad.render(self.prog)

if __name__ == "__main__":
    mglw.run_window_config(Runa)

