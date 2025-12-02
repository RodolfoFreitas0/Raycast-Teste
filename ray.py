import pygame
import math
from settings import *

def normalizeAngle(angle):
    angle = angle % (2 * math.pi)
    if angle <= 0:
        angle = (2 * math.pi) + angle
    return angle

def distanciaEntre(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

class Ray:
    def __init__(self, angle, player, map):
        self.rayAngle = normalizeAngle(angle)
        self.player = player
        self.map = map

        self.down = self.rayAngle > 0 and self.rayAngle < math.pi
        self.up = not self.down
        self.right = self.rayAngle < 0.5 * math.pi or self.rayAngle > 1.5 * math.pi
        self.left = not self.right

        self.hit_x = 0
        self.hit_y = 0

        self.distance = 0

        self.color = 255

    def cast(self):
        
        # Check de parede horizontal

        # h_wall = Horizontal_Wall
        # h_hit = Horizontal_Hit

        h_wall = False
        h_hit_x = 0
        h_hit_y = 0

        # f_Inter = First_Intersection

        f_inter_x = None
        f_inter_y = None

        if self.up:
            f_inter_y = ((self.player.y) // TILESIZE) * TILESIZE - 0.01
        elif self.down:
            f_inter_y = ((self.player.y) // TILESIZE) * TILESIZE + TILESIZE

        f_inter_x = self.player.x + (f_inter_y - self.player.y) / math.tan(self.rayAngle)

        # next_h = Next_Horizontal

        next_h_x = f_inter_x
        next_h_y = f_inter_y

        # "xa" e "ya" é basicamente o espaço entre 1 tile e outro dependendo do angulo do jogador

        xa = 0
        ya = 0

        if self.up:
            ya = -TILESIZE
        elif self.down:
            ya = TILESIZE
        
        xa = ya / math.tan(self.rayAngle)

        # Enquanto estiver dentro da tela
        while (next_h_x <= WINDOW_WIDTH and next_h_x >= 0 and next_h_y <= WINDOW_HEIGHT and next_h_y >= 0):
            if self.map.has_wall_at(next_h_x, next_h_y):
                h_wall = True
                h_hit_x = next_h_x
                h_hit_y = next_h_y
                break
            else:
                next_h_x += xa
                next_h_y += ya

        # TESTE        
        # self.hit_x = h_hit_x
        # self.hit_y = h_hit_y

        # Check de parede vertical

        # v_wall = Vertical_Wall
        # v_hit = Vertical_Hit

        v_wall = False
        v_hit_x = 0
        v_hit_y = 0

        if self.right:
            f_inter_x = (self.player.x // TILESIZE) * TILESIZE + TILESIZE
        elif self.left:
            f_inter_x = (self.player.x // TILESIZE) * TILESIZE - 0.01
        
        f_inter_y = self.player.y + (f_inter_x - self.player.x) * math.tan(self.rayAngle)

        # next_v = Next_Vertical

        next_v_x = f_inter_x
        next_v_y = f_inter_y

        if self.right:
            xa = TILESIZE
        elif self.left:
            xa = -TILESIZE

        ya = xa * math.tan(self.rayAngle)

        while (next_v_x <= WINDOW_WIDTH and next_v_x >= 0 and next_v_y <= WINDOW_HEIGHT and next_v_y >= 0):
            if self.map.has_wall_at(next_v_x, next_v_y):
                v_wall = True
                v_hit_x = next_v_x
                v_hit_y = next_v_y
                break
            else:
                next_v_x += xa
                next_v_y += ya
        
        # Calculo da Distancia

        # h_dist = Horizontal Distance
        # v_dist = Vertical Distance

        h_dist = 0
        v_dist = 0

        if h_wall:
            h_dist = distanciaEntre(self.player.x, self.player.y, h_hit_x, h_hit_y)
        else:
            h_dist = 99999 # Valor do numero não importa, so deve ser grande

        if v_wall:
            v_dist = distanciaEntre(self.player.x, self.player.y, v_hit_x, v_hit_y)
        else:
            v_dist = 99999

        if h_dist < v_dist:
            self.hit_x = h_hit_x
            self.hit_y = h_hit_y
            self.distance = h_dist
            self.color = 160
        else:
            self.hit_x = v_hit_x
            self.hit_y = v_hit_y
            self.distance = v_dist
            self.color = 255

        self.distance *= math.cos(self.player.angle - self.rayAngle)

        self.color *= (30 / self.distance)
        if self.color > 255:
            self.color = 255
        elif self.color < 0:
            self.color = 0

    def render(self, screen):
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (self.player.x, self.player.y),
            (self.hit_x, self.hit_y)
        )