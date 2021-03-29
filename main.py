import pygame as pg
import sys
from pygame.sprite import Group
from bug import Bug


pg.init()

def run_game():

    screen = pg.display.set_mode((1280, 764))
    pg.display.set_caption('Life')
    bugs = Group()
    bugs.add(Bug(20, (200, 200, 200), screen, x=300, y=300))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        screen.fill((0, 0, 0))
        for bug in bugs:
            bug.update(movement=(-0.08, -0.01), rotation=0.1)
        for bug in bugs:
            bug.draw_bug()
        pg.display.flip()


run_game()