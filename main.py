import pygame as pg
import sys
from pygame.sprite import Group
from bug import Bug
from map import Map
from random import randint
from plants import Yavanna


pg.init()

def run_game():

    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption('Life')

    map = Map(screen, weight=255, bias=127, pixel_size=40,
              offsetx=randint(-1000, +1000),
              offsety=randint(-1000, +1000))
              #)
    # bias sets the middle value for the map, while weight defines how far
    # other values are from the middle value.
    yavanna = Yavanna(map, screen)

    bugs = Group()
    bugs.add(Bug(20, (200, 200, 200), screen, x=300, y=300, map=map))
    map.blitme()
    yavanna.draw_trees()
    pg.display.update()

    while True:
        rects_to_update = []

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        for bug in bugs:
            bug.update(movement=(-0.08, -0.01), rotation=0.1)
            bug.draw_bug()
            rects_to_update.extend([bug, bug.left_eye, bug.right_eye])
        pg.display.update(rects_to_update)


run_game()
