import moderngl_window as mglw
import time

WIDTH, HEIGHT = 800, 800


class Runa(mglw.WindowConfig):
    resource_dir = "shaders"  # built in prefix, how neat is that??
    window_size = WIDTH, HEIGHT # same with windows, so convienent
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = self.load_program(vertex_shader=)
