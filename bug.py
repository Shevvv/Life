import pygame as pg
from pygame.sprite import Sprite
import math

class Bug(Sprite):

    def __init__(self, size, color, screen, x=0, y=0):
        super().__init__()
        self.screen = screen
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.direct = 270 # direction in degrees

    def update(self, movement, rotation):
        self.direct += rotation
        self.x += movement[0]
        self.y += movement[1]

    def draw_bug(self):
        body = pg.draw.circle(self.screen,
            self.color,
            (int(self.x + self.size), int(self.y + self.size)),
            self.size)
        _left_eye_center_x = int(body.centerx +
                                 self.size *
                                 math.cos(math.radians(self.direct - 30)))
        _left_eye_center_y = int(body.centery +
                                 self.size *
                                 math.sin(math.radians(self.direct - 30)))
        _right_eye_center_x = int(body.centerx +
                                  self.size *
                                  math.cos(math.radians(self.direct + 30)))
        _right_eye_center_y = int(body.centery +
                                  self.size *
                                  math.sin(math.radians(self.direct + 30)))
        pg.draw.circle(self.screen,
            (255, 0, 0),
            (_left_eye_center_x, _left_eye_center_y),
            2)
        pg.draw.circle(self.screen,
            (255, 0, 0),
            (_right_eye_center_x, _right_eye_center_y),
            2)