# -*- coding: utf-8 -*-

'''
Created on 15/02/2014

@author: DaGal
'''


from Camera import *
from Characters.Mr_H import Mr_H
from Characters.Nazist import Nazist
from Level import Level
from LevelFour import LevelFour
from Resources import *
from Weapons.WpnGrenade import WpnGrenade
from Weapons.WpnRifle import WpnRifle
from Events import *


import Constants
import pygame

class LevelThree(Level):
	def __init__(self, director, player):
		Level.__init__(self, director, player)
		self.player.rect.x = 766
		self.player.rect.y = 82

		self.enemyGroup.add([Nazist(640, 140, self.player, director),
# 							Nazist(640, 176, self.player, director),
# 							Nazist(688, 18, self.player, director),
							Nazist(524, 51, self.player, director),
# 							Nazist(524, 140, self.player, director),
							Nazist(345, 46, self.player, director),
							Nazist(345, 70, self.player, director),
# 							Nazist(345, 100, self.player, director),
							Nazist(140, 145, self.player, director),
							Nazist(140, 175, self.player, director),
							Nazist(185, 10, self.player, director),
							Mr_H(27, 48, self.player, director)])


		self.bg = load_image("mapa_h.png", Constants.MAP_DIR)
		self.collisionBg = load_image("mapa_h_bg.png", Constants.BG_MAP_DIR)

		load_music("level_three.xm")
		pygame.mixer.music.set_volume(0.25)
		pygame.mixer.music.play(-1)

		player.setWeapons([WpnGrenade(), WpnRifle()])

	def processEvent(self, event):
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
			nextLevel = LevelFour(self.director, self.player)
			self.director.setScene(nextLevel)

		if event.type == pygame.USEREVENT and event.code == MRHDEAD:
			nextLevel = LevelFour(self.director, self.player)
			self.director.setScene(nextLevel)

		Level.processEvent(self, event)
