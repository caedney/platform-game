import pygame
from tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
	def __init__(self, size, x, y, path):
		super().__init__(size, x, y, path)
		self.rect.y += size - self.image.get_size()[1]
		self.speed = randint(3, 4)

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image, True, False)

	def reverse(self):
		self.speed *= -1

	def update(self, x_shift):
		super().update(x_shift)
		self.animate()
		self.move()
		self.reverse_image()