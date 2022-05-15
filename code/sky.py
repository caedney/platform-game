from cmath import rect
import pygame
from settings import screen_width, tile_size, vertical_tile_number
from support import import_folder
from random import choice, randint


class Sky:
    def __init__(self, horizon, style = 'level'):
        self.top = pygame.image.load('graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('graphics/decoration/sky/sky_middle.png').convert()
        self.horizon = horizon

        # Stretch
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))

        self.style = style

        if self.style == 'overworld':
            palm_surfaces = import_folder('graphics/overworld/palms')
            self.palms = []

            for surface in [choice(palm_surfaces) for image in range(10)]:
                x = randint(0, screen_width)
                y = (self.horizon * tile_size) + randint(50, 100)
                rect = surface.get_rect(midbottom = (x, y))
                self.palms.append((surface, rect))

            cloud_surfaces = import_folder('graphics/overworld/clouds')
            self.clouds = []

            for surface in [choice(cloud_surfaces) for image in range(10)]:
                x = randint(0, screen_width)
                y = randint(0, (self.horizon * tile_size) - 100)
                rect = surface.get_rect(midbottom = (x, y))
                self.clouds.append((surface, rect))

    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size

            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

        if self.style == 'overworld':
            for palm in self.palms:
                surface.blit(palm[0], palm[1])

            for cloud in self.clouds:
                surface.blit(cloud[0], cloud[1])