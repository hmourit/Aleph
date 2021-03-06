# -*- coding: utf-8 -*-

'''
Created on 16/03/2014

@author: DaGal
'''

from Enemy import Enemy
from Weapons.WpnRifle import WpnRifle
from pygame import event, USEREVENT
from Events import *


class Mr_H(Enemy):
	"""
	Contains logic for Mr_H enemy.
	"""

	def __init__(self, x, y, player, director):
		Enemy.__init__(self, x, y, "mr_h.png", -1, "coordMr_h.txt", [
                       3, 3, 3, 3], player, (0, 10, 6, 10, 6, 4, 6, 8), director)

		# Maybe another kind of weapon?
		self.setWeapon(WpnRifle())
		self.hp = 200


	def check_died(self, scene):
		"""
		Check whether this enemy has died.
		"""
		if self.hp <= 0:
			scene.enemyGroup.remove(self)
			event.post(event.Event(USEREVENT, code=MRHDEAD))
