"""
Idea: currently the Sprite is half written in `screen` coordinates and half
in `map` coordinates. Rewrite the whole thing in `map` coordinates.
"""


import pygame as pg
from pygame.sprite import Sprite
import math

class Bug(Sprite):

    def __init__(self, size, color, screen, map, x=0, y=0, b_color='cyan'):
        # b_color stands for body color, the color visible to other bugs
        super().__init__()
        self.screen = screen
        self.size = size
        self.color = color
        self.b_color = b_color
        self.x = x
        self.y = y
        self.map = map
        self.rect = pg.Rect(self.x, self.y, 2*self.size, 2*self.size)
        self.direct = 270 # direction in degrees

    def update(self, movement, rotation):
        self.direct += rotation
        self.x += movement[0]
        self.y += movement[1]
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw_bug(self):
        self.update_biomes()

        # represent the bug's health
        pg.draw.circle(self.screen,
                       self.color,
                       (self.rect.centerx, self.rect.centery),
                       self.size)

        # represent the bug's visible surface
        pg.draw.circle(self.screen,
            self.b_color,
            (self.rect.centerx, self.rect.centery),
            self.size,
            width=2)

        _left_eye_center_x = int(self.rect.centerx +
                                 self.size *
                                 math.cos(math.radians(self.direct - 30)))
        _left_eye_center_y = int(self.rect.centery +
                                 self.size *
                                 math.sin(math.radians(self.direct - 30)))
        _right_eye_center_x = int(self.rect.centerx +
                                  self.size *
                                  math.cos(math.radians(self.direct + 30)))
        _right_eye_center_y = int(self.rect.centery +
                                  self.size *
                                  math.sin(math.radians(self.direct + 30)))
        self.left_eye = pg.draw.circle(self.screen,
                                       (255, 0, 0),
                                       (_left_eye_center_x,
                                       _left_eye_center_y),
                                       2)
        self.right_eye = pg.draw.circle(self.screen,
                                       (255, 0, 0),
                                       (_right_eye_center_x,
                                       _right_eye_center_y),
                                       2)

        #self.left_leg =

    def update_biomes(self):
        for biome in self.map.biomes:
            if biome.rect.colliderect(self.rect.inflate(6, 6)):
                self.screen.fill(biome.color, biome.rect)
                [tree.draw() for tree in biome.plants.sprites()]

                # pass



