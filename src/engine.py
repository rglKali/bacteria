import numba as nb
import numpy as np
import random as rd
import pygame as pg
from .config import *


class Engine:
    def __init__(self, screen):
        self.screen = screen

        self.bacterias = list()
        for b in range(bacterias):
            radius = rd.random() * 3 + 6
            angle = rd.random() * 2 * np.pi
            pos_x = rd.random() * (res[0] - 2 * radius) + radius
            pos_y = rd.random() * (res[1] - 2 * radius) + radius
            ball = np.array([radius, pos_x, pos_y, np.cos(angle) * (10 - radius), np.sin(angle) * (10 - radius)], dtype=np.float64)
            self.bacterias.append(ball)

        self.bacterias = np.array(self.bacterias)

        self.render(self.bacterias)

    @staticmethod
    @nb.njit(fastmath=True, parallel=True)
    def render(bacterias):
        for num in nb.prange(len(bacterias)):

            # Walls collision
            if bacterias[num][1] - bacterias[num][0] < 0:
                bacterias[num][3] *= -1
                bacterias[num][1] = bacterias[num][0]
            elif bacterias[num][1] + bacterias[num][0] > res[0]:
                bacterias[num][3] *= -1
                bacterias[num][1] = res[0] - bacterias[num][0]

            if bacterias[num][2] - bacterias[num][0] < 0:
                bacterias[num][4] *= -1
                bacterias[num][2] = bacterias[num][0]
            elif bacterias[num][2] + bacterias[num][0] > res[1]:
                bacterias[num][4] *= -1
                bacterias[num][2] = res[1] - bacterias[num][0]

            # Collision between bacterias
            for n in nb.prange(num):
                distance = np.sqrt((bacterias[num][1] - bacterias[n][1]) ** 2 + (bacterias[num][2] - bacterias[n][2]) ** 2)
                if distance <= bacterias[num][0] + bacterias[n][0]:

                    dx = bacterias[num][3] - bacterias[n][3]
                    dy = bacterias[num][4] - bacterias[n][4]

                    bacterias[num][3] = dx * (bacterias[num][0] - bacterias[n][0]) / (bacterias[num][0] + bacterias[n][0]) + bacterias[n][3]
                    bacterias[num][4] = dy * (bacterias[num][0] - bacterias[n][0]) / (bacterias[num][0] + bacterias[n][0]) + bacterias[n][4]

                    bacterias[n][3] = 2 * dx * bacterias[num][0] / (bacterias[num][0] + bacterias[n][0]) + bacterias[n][3]
                    bacterias[n][4] = 2 * dy * bacterias[num][0] / (bacterias[num][0] + bacterias[n][0]) + bacterias[n][4]

                    bacterias[num][1] = bacterias[num][1] - dx * bacterias[num][0] / (bacterias[num][0] + bacterias[n][0])
                    bacterias[num][2] = bacterias[num][2] - dy * bacterias[num][0] / (bacterias[num][0] + bacterias[n][0])

                    bacterias[n][1] = bacterias[n][1] + dx * bacterias[n][0] / (bacterias[num][0] + bacterias[n][0])
                    bacterias[n][2] = bacterias[n][2] + dy * bacterias[n][0] / (bacterias[num][0] + bacterias[n][0])

            # Movement
            bacterias[num][1] += bacterias[num][3]
            bacterias[num][2] += bacterias[num][4]

    def draw(self):
        [pg.draw.circle(self.screen, colors[int((b[0] - 6) * 5)], (b[1], b[2]), b[0]) for b in self.bacterias]

    def run(self):
        self.render(self.bacterias)
        self.draw()
