import pygame as pg
from pygame.sprite import Sprite, Group
from numpy.random import normal
from random import randint, choices
from noise import snoise2

def memoize(f):
    def helper(x):
        helper.calls += 1
        f(x)

    helper.calls = 0
    return helper

class Yavanna():

    def __init__(self, map, screen):
        super().__init__()
        self.biomes = map.biomes
        self.pixel_size = map.pixel_size
        self.screen = screen
        self.algae = []
        self.init_populate()

    # This works at pixel size 32 and greater (basically, any value whose
    # square is grater than 1000, since `t_factor` are in the range of 10^-3).
    # Make it less than that, and the `t_factor`becomes less and less
    # significant, to the point of becoming non relevant at pixel size 1
    # (basically int vs float conflict).
    def init_populate(self):
        extend_algea = False

        for biome in self.biomes:
            if biome.name == 'sea':
                Plant = Alga
                extend_algea = True

            else:
                Plant = Tree
            max_density = biome.t_factor * self.pixel_size ** 2
            biome.max_density = max_density

            plants_coords = []
            number_of_trees = normal(loc=max_density,
                                     scale=self.pixel_size * 0.01,
                                     size=1) if max_density != 0 else 0
            if number_of_trees > max_density: number_of_trees = max_density


            while len(plants_coords) < number_of_trees:
                plant_x = randint(0, self.pixel_size)
                plant_y = randint(0, self.pixel_size)
                if (plant_x, plant_y) in plants_coords:
                    continue
                else:
                    plants_coords.append((plant_x, plant_y))

            plants = Group()

            for i, plant in enumerate(plants_coords):
                plants.add(Plant(plant[0], plant[1], self.screen, biome,
                             self.pixel_size, noise_y=i))
            if extend_algea:
                self.algae.extend(plants)

            biome.plants = plants

    # The alternative to the original `self.init_populate`. Super slow,
    # but always correct, no matter the pixel size.
    def alt_init_populate(self):
        for biome in self.biomes:
            max_density = biome.t_factor * self.pixel_size ** 2
            biome.max_density = max_density

            plants_coords = []
            for x in range(self.pixel_size):
                for y in range(self.pixel_size):
                    if choices((0, 1), [1 - max_density, max_density])[0]:
                        plants_coords.append((x, y))

            plants = Group()

            for plant in plants_coords:
                plants.add(Tree(plant[0], plant[1], self.screen, biome,
                             self.pixel_size))

            biome.plants = plants

    def draw_trees(self):
        for biome in self.biomes:
            for plant in biome.plants.sprites():
                plant.draw()
    
    


class Tree(Sprite):

    def __init__(self, x, y, screen, biome, pixel_size, **kwargs):
        super().__init__()
        self.x = x
        self.y = y
        self.screen = screen
        self.biome = biome
        self.pixel_size = pixel_size

    def draw(self):
        self.rect = pg.Rect(self.x + self.biome.x * self.pixel_size,
                    self.y + self.biome.y * self.pixel_size,
                    1, 1)

        self.screen.fill((0, 0, 0), self.rect)

class Alga(Tree):

    def __init__(self, x, y, screen, biome, pixel_size, **kwargs):
        super().__init__(x, y, screen, biome, pixel_size, **kwargs)

        self.octaves = 64
        self.freq = 16 * self.octaves
        self.noise_y = kwargs['noise_y']

    # Currently restricted to its biome for the sake of simplicity
    @memoize
    def update(self):
        self.x += 3 * snoise2(self.update.calls,
                          self.noise_y,
                          self.octaves)
        self.y += 3 * snoise2(self.noise_y,
                          self.update.calls,
                          self.octaves)

        if self.x >= self.pixel_size:
            self.x = self.pixel_size - 1
        elif self.x < 0:
            self.x = 0

        if self.y >= self.pixel_size:
            self.y = self.pixel_size - 1
        elif self.y < 0:
            self.y = 0

