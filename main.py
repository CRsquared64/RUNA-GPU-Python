import os
import gui
import simulations
# import moderngl_window as mglw
import rune
import queue
import pickle

WIDTH, HEIGHT = 600, 800
position_queue = queue.Queue()
RuneApp = gui.RuneGUI(WIDTH, HEIGHT, position_queue)
RuneApp()
print("App Closed, Simulations Firing Up")
for filename in os.listdir("cache/"):
    if filename.endswith(".nbody"):
        with open(f"cache/{filename}", "rb") as file:
            sim_data = pickle.load(file)
            pos, name, n, g, dt, vel = sim_data
            mglw = rune.return_mglw()
            sim = rune.Runa(pos,vel,g,n,dt)
            mglw.run_window_config(sim)
