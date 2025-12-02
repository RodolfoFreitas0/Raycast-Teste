import pygame
import math
from settings import *

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH / 2 
        self.y = WINDOW_HEIGHT / 2
        self.radius = 3
        self.angle = 0
        self.rotSpeed = 2.5 * (math.pi / 180)
        self.rotation = 0 # -1: esquerda, 0: parado, 1: direita

        self.movement = 0 # -1: trás, 0: parado, 1: frente
        self.speed = 1.5

    def update(self):

        keys = pygame.key.get_pressed()

        self.rotation = 0
        self.movement = 0

        if keys[pygame.K_RIGHT]:
            self.rotation = 1
        if keys[pygame.K_LEFT]:
            self.rotation = -1
        if keys[pygame.K_UP]:
            self.movement = 1
        if keys[pygame.K_DOWN]:
            self.movement = -1

        moveStep = self.movement * self.speed
        self.angle += self.rotation * self.rotSpeed
        self.x += math.cos(self.angle) * moveStep
        self.y += math.sin(self.angle) * moveStep

    def render(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)