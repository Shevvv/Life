import pygame as pg
from pygame.sprite import Sprite
from numpy.random import normal
from random import randint

class Yavanna():

    def __init__(self, map, screen):
        super().__init__()
        self.biomes = map.biomes
        self.pixel_size = map.pixel_size
        self.screen = screen
        self.init_populate()

    def init_populate(self):
        for biome in self.biomes:
            max_density = biome.t_factor * self.pixel_size ** 2
            biome.max_density = max_density

            trees_coords = []
            number_of_trees = int(normal(loc=max_density,
                                     scale=0.05,
                                     size=1)) if max_density != 0 else 0

            while len(trees_coords) < number_of_trees:
                tree_x = randint(0, self.pixel_size)
                tree_y = randint(0, self.pixel_size)
                if (tree_x, tree_y) in trees_coords:
                    continue
                else:
                    trees_coords.append((tree_x, tree_y))

            trees = []

            for tree in trees_coords:
                trees.append(Tree(tree[0], tree[1], self.screen, biome,
                             self.pixel_size))

            biome.trees = trees

    def draw_trees(self):
        for biome in self.biomes:
            for tree in biome.trees:
                tree.draw()


class Tree(Sprite):

    def __init__(self, x, y, screen, biome, pixel_size):
        super().__init__()
        self.x = x
        self.y = y
        self.screen = screen
        self.biome = biome
        self.pixel_size = pixel_size

    def draw(self):
        self.screen.fill((0, 0, 0),
            pg.Rect(self.x + self.biome.x * self.pixel_size,
                    self.y + self.biome.y * self.pixel_size,
                    1, 1))
