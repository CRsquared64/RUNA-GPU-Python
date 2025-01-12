import os
import gui
import simulations
import rune
import queue
import pickle

import pygame

import QuadTree.quadTree as quadTree


WIDTH, HEIGHT = 600, 800
position_queue = queue.Queue()
RuneApp = gui.RuneGUI(WIDTH, HEIGHT, position_queue)
RuneApp()
print("App Closed, Simulations Firing Up")
for filename in os.listdir("cache/"):
    if filename.endswith(".nbody"):
        with open(f"cache/{filename}", "rb") as file:
            sim_data = pickle.load(file)
            pos, name, n, g, dt, vel, isPython = sim_data
            print(isPython)
            if isPython == 0:
                rune.run(pos,vel, g, n, dt)
            elif isPython == True:
                import QuadTree.traverseGraph as traverse
                pygame.init()
                pygame.display.set_caption("Nbody 2")
                clock = pygame.time.Clock()

                size = 1000
                window_x = 800
                window_y = 800
                screen = pygame.display.set_mode((window_x, window_y))
                bodies = quadTree.np_to_body(pos, vel, float(g), float(dt))
                while True:
                    screen.fill((10,10,10))
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            bodies = traverse.click_spawn(bodies)
                    bodies = traverse.render_frame(bodies)
                    pygame.display.update()
                    clock.tick(120)

