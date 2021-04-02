import pygame as pg
import sys
from pygame.sprite import Group
from bug import Bug
from map import Map
from random import randint
from plants import Yavanna
from settings import Settings


pg.init()

def run_game():

    s = Settings()
    screen = pg.display.set_mode(s.display_size)
    pg.display.set_caption('Life')

    map = Map(screen, weight=s.weight, bias=s.bias, pixel_size=s.pixel_size,
              offsetx=randint(-1000, +1000),
              offsety=randint(-1000, +1000))
              #)
    # bias sets the middle value for the map, while weight defines how far
    # other values are from the middle value.
    yavanna = Yavanna(map, screen)

    bugs = Group()
    bugs.add(Bug(s.bug_size, s.bug_color, screen, map, s._x, s._y))
    map.blitme()
    yavanna.draw_trees()
    pg.display.update()

    while True:
        rects_to_update = []

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        for bug in bugs:
            bug.update(s._movement, s._rotation)
            bug.draw_bug()
            rects_to_update.extend([bug, bug.left_eye, bug.right_eye])
        pg.display.update(rects_to_update)


run_game()
