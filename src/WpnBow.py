# -*- coding: utf-8 -*-

'''
Created on 09/03/2014

@author: DaGal
'''

from Item import *
from Constants import *
import math

class WpnBow(Item):
	def __init__(self, x, y, imageName=None, colorkey=None, clipRect=None):
		Item.__init__(self, x, y, imageName, colorkey, clipRect)

	def update(self, time, char):
		self.rect.clamp_ip(char.rect)

		# This magic numbers could be offsets specified for each character
		if char.posIndex == POS_RIGHT:
			self.angle = 0
			self.rect.center = (char.rect.right - 4, char.rect.centery + 8)
			self.flipH = True
			self.flipV = False
		elif char.posIndex == POS_LEFT:
			self.angle = 0
			self.rect.center = (char.rect.left + 4, char.rect.centery + 6)
			self.flipH = False
			self.flipV = False
		elif char.posIndex == POS_UP:
			self.angle = -25
			self.rect.center = (char.rect.right - 2, char.rect.centery + 8)
			self.flipH = True
			self.flipV = False
		elif char.posIndex == POS_DOWN:
			self.angle = -25
			self.rect.center = (char.rect.left, char.rect.centery + 8)
			self.flipH = True
			self.flipV = True

		if char.attacking:
			print "attack"