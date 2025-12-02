import pygame

from map import Map
from player import Player
from raycaster import Raycaster

from settings import *

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

map = Map()
player = Player()

clock = pygame.time.Clock()
raycaster = Raycaster(player, map)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill((0, 0, 0))

    player.update()
    raycaster.castRays()

    if MODE_2D:
        map.render(screen)
        player.render(screen)

    raycaster.render(screen)

    pygame.display.update()