import pygame
from settings import screen_width, tile_size, vertical_tile_number


class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load('graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('graphics/decoration/sky/sky_middle.png').convert()
        self.horizon = horizon

        # Stretch
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))

    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size

            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))