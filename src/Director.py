# -*- coding: utf-8 -*-

'''
Created on 03/03/2014

@author: DaGal
'''

import pygame
import sys
from GameScene import *
from Camera import *
from Player import Player
from MainMenu import MainMenu

class Director():

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), 0, 32)
		pygame.display.set_caption("The white square adventures")
		self.player = Player(200, 200)
		# It's good to have player here because we can preserve it easily between levels
# 		self.scene = GameScene(self, self.player)
		self.scene = MainMenu(self)
		self.clock = pygame.time.Clock()

	def loop(self):
		exitGame = False

		while not exitGame:
			elapsedTime = self.clock.tick(60)

			for event in pygame.event.get():
				exitGame = event.type == pygame.QUIT
				self.scene.processEvent(event)

			self.scene.update(elapsedTime)
			self.scene.draw(self.screen)
			pygame.display.flip()

		return exitGame

	def enqueueEvent(self, event):
		pygame.event.post(event)
	
	def setScene(self, scene):
		self.scene = scene