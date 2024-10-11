import math
import numpy as np
import random
from tqdm import tqdm

def uniform_square(n):
    r = int(math.sqrt(n))
    pos = []

    scale_factor = 2 / (r - 1)

    for i in range(r):
        for j in range(r):
            x = i * scale_factor - 1
            y = j * scale_factor - 1
            z = 0
            mass = 1
            pos.append([x, y, z, mass])

    vel = np.zeros((n, 4))
    return np.array(pos), vel


def square(n):
    pos = np.random.uniform(-1.0, 1.0, (n, 2))
    z = np.zeros((n, 1))
    pos = np.hstack((pos, z))

    mass = np.ones((n, 1))
    pos = np.hstack((pos, mass))

    vel = np.zeros((n, 4))

    return pos, vel


def circle(n):
    min_dist = 0.05
    pos = [[0, 0, 0, 10000]]
    vel = [[0, 0, 0,1]]
    with tqdm(total=n-1) as pbar:
        for i in range(n - 1):
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

            vel.append([xv, yv, zv, 0])
            pbar.update(1)
    return np.array(pos), np.array(vel)

