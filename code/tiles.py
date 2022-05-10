import pygame
from support import import_folder


class Tile(pygame.sprite.Sprite):
	def __init__(self, size, x, y):
		super().__init__()
		self.image = pygame.Surface((size, size))
		self.rect = self.image.get_rect(topleft = (x, y))

	def update(self, x_shift):
		self.rect.x += x_shift


class StaticTile(Tile):
	def __init__(self, size, x, y, surface):
		super().__init__(size, x, y)
		self.image = surface


class CrateTile(StaticTile):
	def __init__(self, size, x, y, surface):
		super().__init__(size, x, y, surface)
		offset_y = y + size
		self.rect = self.image.get_rect(bottomleft = (x, offset_y))


class AnimatedTile(Tile):
	def __init__(self, size, x, y, path):
		super().__init__(size, x, y)
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

	def animate(self):
		self.frame_index += 0.15

		if self.frame_index >= len(self.frames):
			self.frame_index = 0

		self.image = self.frames[int(self.frame_index)]

	def update(self, x_shift):
		self.animate()
		super().update(x_shift)


class CoinTile(AnimatedTile):
	def __init__(self, size, x, y, path):
		super().__init__(size, x, y, path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 2)
		self.rect = self.image.get_rect(center = (center_x, center_y))


class PalmTile(AnimatedTile):
	def __init__(self, size, x, y, path, offset):
		super().__init__(size, x, y, path)
		offset_y = y - offset
		self.rect.topleft = (x, offset_y)
