# -*- coding: utf-8 -*-

'''
Created on 03/03/2014

@author: DaGal
'''

# -*- coding: utf-8 -*-

from Character import Character
import pygame
import Util

PLAYER_SPEED = 0.25


class Player(Character):
	def __init__(self, x, y, *args):
		Character.__init__(self, x, y)
		self.rect = pygame.Rect(x, y, 18, 27)

		self.sheet = Util.load_image("player-alt.png", "../media/sprites", -1)

	def update(self, time, collisionMap):
		keys = pygame.key.get_pressed()
		self.speedX = 0
		self.speedY = 0

		if keys[pygame.K_s]:
			self.speedY = PLAYER_SPEED
		elif keys[pygame.K_w]:
			self.speedY = -PLAYER_SPEED
		if keys[pygame.K_a]:
			self.speedX = -PLAYER_SPEED
		elif keys[pygame.K_d]:
			self.speedX = PLAYER_SPEED

		self.move(time, collisionMap)

	def draw(self, screen, camera):
		screen.blit(self.sheet, camera.apply(self), pygame.Rect(99, 70, 18, 27))
