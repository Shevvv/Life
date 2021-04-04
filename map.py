from noise import snoise2
import pygame as pg
from math import ceil

class Map(pg.Surface):


    def __init__(self, screen, pixel_size=1, offsetx=0, offsety=0,
            weight=128, bias=127, grayscale=False):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.pixel_size = pixel_size
        self.offsetx = offsetx
        self.offsety = offsety
        self.weight = weight
        self.bias = bias
        super().__init__((self.screen_rect.width, self.screen_rect.height))

        self.octaves = 64
        self.freq = 16 * self.octaves

        self.map = []
        self.max_height = self.weight + self.bias
        for y in range(self.screen_rect.height):
            _line = []
            for x in range(self.screen_rect.width):
                _line.append(int(snoise2(x / self.freq + self.offsetx,
                                         y / self.freq + self.offsety,
                                         self.octaves) * self.weight +
                                                         self.bias))
            self.map.append(_line)

        self.map_biomes(grayscale=grayscale)

    def pixelize(self):
        _incomplete_pixels =\
            [[] for _ in range(ceil(self.screen_rect.width / self.pixel_size))]
        self.pixels = []

        for y, line in enumerate(self.map):
            j = 0
            _pixel_size = self.pixel_size

            for x, _pixel in enumerate(line):
                # print(f'{j}, {len(line)}, f'{_pixel_size}')
                _incomplete_pixels[j].append(_pixel)
                if (x + 1) % self.pixel_size == 0:
                    j += 1
                    if len(line) - self.pixel_size * j < self.pixel_size:
                        _pixel_size = len(line) % self.pixel_size
                # increment j if reached the size of a pixel, which depends
                # on how close to the line edge the loop is.

            if (y + 1) % self.pixel_size == 0 or (y + 1) == len(self.map):
                self.pixels.append([])
                for pixel in _incomplete_pixels:
                    self.pixels[-1].append(sum(pixel) / len(pixel))
                    _incomplete_pixels = [[] for _ in range(
                            ceil(self.screen_rect.width / self.pixel_size))]

    def map_biomes(self, sea_level=63, steppe_level=127, desert_level=191,
            grayscale=False):

        self.sea = []

        if self.pixel_size != 1:
            self.pixelize()
        else:
            self.pixels = self.map
        self.biomes = []
        for y, line in enumerate(self.pixels):
            for x, pixel in enumerate(line):
                biome = None
                if grayscale:
                    if pixel < 0:
                        shade = 0
                    elif pixel > 255:
                        shade = 255
                    else:
                        shade = pixel
                    color = (shade, shade, shade)
                    t_factor= 0
                elif pixel < sea_level:
                    color = (0, 0, 255) # sea
                    biome = 'sea'
                    t_factor = 0.01
                elif sea_level <= pixel < steppe_level:
                    color = (0 , 100, 0) # land
                    biome = 'land'
                    t_factor = 0.016
                elif steppe_level <= pixel < desert_level:
                    color = (124, 252, 0) # steppe
                    biome = 'steppe'
                    t_factor = 0.007
                else:
                    color = (255, 255, 0) # desert
                    biome = 'desert'
                    t_factor = 0.001
                rect_to_fill = pg.Rect(x * self.pixel_size,
                                       y * self.pixel_size,
                                       self.pixel_size,
                                       self.pixel_size)
                biome = Biome((x, y), biome, t_factor, rect_to_fill,
                              self.screen, color)
                if biome.name == 'sea':
                    self.sea.append(biome)
                self.biomes.append(biome)
                self.fill(color, rect_to_fill)

    def blitme(self):
        self.screen.blit(self, self.screen_rect)

class Biome():

    def __init__(self, coords, biome, t_factor, rect, screen, color):
        self.x = coords[0]
        self.y = coords[1]
        self.rect = rect
        self.screen = screen
        self.name = biome
        self.t_factor = t_factor
        self.color = color

        self.max_density = None
        self.plants = []

    def draw(self):
        plant_rects = []

        plant_rects.append(self.rect)
        self.screen.fill(self.color, self.rect)

        return plant_rects

