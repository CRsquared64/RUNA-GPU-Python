import math
import numpy as np
import random

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
    return np.array(pos), np.array(vel)

"""
   def uniform_square(self):
        r = int(math.sqrt(self.n))
        pos = []

        scale_factor = (2 / (r - 1))

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

        pos = np.random.uniform(-1, 1, (self.n, 2))
        z = np.zeros((self.n, 1))
        pos = np.hstack((pos, z))

        mass = np.ones((self.n, 1))
        pos = np.hstack((pos, mass))

        vel = np.zeros((self.n,4))

        return pos, vel

    def square_rotate(self):
        r = int(math.sqrt(self.n))
        pos = []
        vel = []

        scale_factor = (2 / (r - 1))

        for i in range(r):
            for j in range(r):

                x = i * scale_factor - 1
                y = j * scale_factor - 1
                z = 0
                mass = 1
                pos.append([x, y, z, mass])
                xv = -y * 0.001
                yv = x * 0.001
                zv = 0
                padding = 1
                vel.append([xv,yv,zv,padding])


        return np.array(pos), vel

    def circle(self):
        min_dist = 0
        pos = [[0, 0, 0, 1000]]
        vel = [[0, 0, 0,0]]
        for i in range(self.n - 1):
            angle = random.random() * math.pi * 2
            distance = (random.random()) * 1 + min_dist

            x = math.cos(angle) * distance * 1
            y = math.sin(angle) * distance * 1
            z = 0
            mass = 1

            pos.append([x, y, z, mass])

            xv = math.cos(angle + math.pi / 2) * distance * 500
            yv = math.sin(angle + math.pi / 2) * distance * 500
            zv = 0

            vel.append([xv, yv, zv,0])
        return np.array(pos), np.array(vel)

    def spiral(self):
        arm_separation = np.pi
        noise_std = 0.4
        a  = 0.1
        b = 0.3
        n_arm_points = self.n // 2  # Points per arm
        theta = np.linspace(0, 4 * np.pi, n_arm_points)  # Angle range for one arm

        # Spiral equation for radius
        r = a + b * theta  # r = a + b * theta

        # First arm
        x1 = r * np.cos(theta)
        y1 = r * np.sin(theta)

        # Second arm (shifted by `arm_separation`)
        x2 = r * np.cos(theta + arm_separation)
        y2 = r * np.sin(theta + arm_separation)

        # Combine both arms
        x = np.concatenate([x1, x2])
        y = np.concatenate([y1, y2])

        x += np.random.normal(0, noise_std, size=x.shape)
        y += np.random.normal(0, noise_std, size=y.shape)
        # Normalize x and y to the range [-1, 1]


        # Create z values (all 0) and mass values (all 1)
        z = np.zeros_like(x)
        mass = np.ones_like(x)

        distance = np.sqrt(x ** 2 + y ** 2)  # Radial distance in 2D
        angle = np.arctan2(y, x)  # Angle in 2D (from x-axis)

        # Compute velocity components (rotated by 90 degrees)
        xv = np.cos(angle + np.pi / 2) * distance * 100
        yv = np.sin(angle + np.pi / 2) * distance * 100
        zv = np.zeros_like(xv)  # Since all motion is in the xy-plane
        p  = np.ones_like(xv)

        vel = np.column_stack([xv,yv,zv,p])

        # Stack the results into a (n_points, 4) array
        galaxy = np.column_stack([x, y, z, mass])
        return galaxy, vel

    def system(self):
        sun_n = (self.n // 100) * 97
        planet_n = (self.n // 100) * 3

        pos = []
        vel = []
        for i in range(sun_n):
            angle = random.random() * math.pi * 2
            distance = (random.random()) * 0.05

            x = math.cos(angle) * distance * 1
            y = math.sin(angle) * distance * 1
            z = 0
            mass = 1

            pos.append([x, y, z, mass])

            xv = math.cos(angle + math.pi / 2) * distance * 5000
            yv = math.sin(angle + math.pi / 2) * distance * 5000
            zv = 0

            vel.append([xv, yv, zv, 0])

        for i in range(planet_n):
            angle = random.random() * math.pi * 2
            distance = (random.random()) * 0.01

            x = math.cos(angle) * distance * 1 - 2
            y = math.sin(angle) * distance * 1
            z = 0
            mass = 1

            pos.append([x, y, z, mass])
            xv = 0
            yv = -120
            zv = 0

            vel.append([xv, yv, zv, 0])

        remaning = self.n - len(pos)
        if remaning:
            for i in range(remaning):
                pos.append([0,0,0,1])
                vel.append([0,0,0,1])
        return np.array(pos), np.array(vel)


    def galaxy_collision(self):
        min_dist = 0.002
        pos = []
        vel = []
        for i in range((self.n) // 2):
            angle = random.random() * math.pi * 2
            distance = (random.random()) * 0.2 + min_dist

            x = math.cos(angle) * distance * 1 + 2
            y = math.sin(angle) * distance * 1 + 2
            z = 0
            mass = 1

            pos.append([x, y, z, mass])

            xv = math.cos(angle + math.pi / 2) * distance * 800
            yv = math.sin(angle + math.pi / 2) * distance * 800
            zv = 0

            vel.append([xv, yv, zv, 0])

        for i in range((self.n) // 2):
            angle = random.random() * math.pi * 2
            distance = (random.random()) * 0.2 + min_dist

            x = math.cos(angle) * distance * 1 - 2
            y = math.sin(angle) * distance * 1 - 2
            z = 0
            mass = 1

            pos.append([x, y, z, mass])

            xv = math.cos(angle + math.pi / 2) * distance * 550
            yv = math.sin(angle + math.pi / 2) * distance * 550
            zv = 0

            vel.append([xv, yv, zv, 0])

        remaining = len(pos) - self.n

        return np.array(pos), np.array(vel)
"""