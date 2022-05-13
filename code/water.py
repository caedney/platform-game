import pygame
from settings import screen_width
from tiles import AnimatedTile


class Water:
    def __init__(self, top, level_width):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(water_tile_width, x, y, 'graphics/decoration/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, x_shift):
        self.water_sprites.update(x_shift)
        self.water_sprites.draw(surface)