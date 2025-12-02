import pygame
import math
from settings import *
from ray import Ray

class Raycaster:
    def __init__(self, player, map):
        self.rays = []
        self.player = player
        self.map = map
    
    def castRays(self):
        self.rays = []
        rayAngle = (self.player.angle - FOV / 2)
        for i in range(NUM_RAYS):
            ray = Ray(rayAngle, self.player, self.map)
            ray.cast()
            self.rays.append(ray)

            rayAngle += FOV / NUM_RAYS

    def render(self, screen):

        counter = 0
        for ray in self.rays:
            if MODE_2D:
                ray.render(screen)

            else:
                line_height = (32 / ray.distance) * 415

                # d_ = Draw

                d_begin = (WINDOW_HEIGHT / 2) - (line_height / 2)
                d_end = line_height

                pygame.draw.rect(screen, (ray.color, ray.color, ray.color), (counter * RES, d_begin, RES, d_end))

                counter += 1