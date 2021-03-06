# -*- coding: utf-8 -*-

'''
Created on 16/03/2014

@author: DaGal
'''

from pygame import Rect, sprite
from Bullet import Bullet
from Characters.Character import isSolid, roundToInt
from Explosion import Explosion

GRENADE_SPEED = 0.3
MAX_THROW_DISTANCE = 150
TIME_TO_BOOM = 2000

class ThrowedGrenade(Bullet):
	def __init__(self,creator, x, y, speedX, speedY, throwDistance):
		Bullet.__init__(self, creator, x, y, speedX, speedY, "items-1small.png", None, Rect(110, 120, 9, 11))
		self.rect = Rect(x, y, 0, 0)
		self.speedX = speedX
		self.speedY = speedY

		# Important if you want pinpoint accuracy
		self.floatX = float(self.rect.x)
		self.floatY = float(self.rect.y)


		if throwDistance > MAX_THROW_DISTANCE:
			throwDistance = MAX_THROW_DISTANCE

		self.timeToStop = throwDistance / GRENADE_SPEED
		self.timeToBoom = TIME_TO_BOOM
		self.atk = 70

	def update(self, time, scene):
		self.floatX += self.speedX * time * GRENADE_SPEED
		self.floatY += self.speedY * time * GRENADE_SPEED
		self.rect.x = roundToInt(self.floatX)
		self.rect.y = roundToInt(self.floatY)

		self.timeToBoom -= time

		if self.timeToBoom <= 0:
			scene.bulletGroup.remove(self)
			scene.bulletGroup.add(Explosion(self.rect.x, self.rect.y))

			# Kill people!
			originalRect = self.rect.copy()
			self.rect.inflate_ip(80, 80)  # 80x80 area damage
			
			enemies_hit = sprite.spritecollide(self, scene.enemyGroup, False)

			for enemy in enemies_hit:
				# Friendly fire
				if self.creator.__class__.__name__ == enemy.__class__.__name__:
					continue
				enemy.receive_attack(self.atk)

			if sprite.collide_rect(self, scene.player):
				scene.player.receive_attack(self.atk)

			self.rect = originalRect  # Restore the real rect

		self.timeToStop -= time

		if self.timeToStop <= 0:
			self.speedX = 0
			self.speedY = 0
