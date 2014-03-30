# -*- coding: utf-8 -*-

from Controller import Controller
from Constants import *
import math
import random
import pygame

DETECTION_RANGE = 200
MAX_TIMES_COLLIDED = 10

class RangeController(Controller):
	"""
	This class contains the logic to manage an Enemy's behavior.
	This is almost a copy of the MeleeController,
	however a more realistic version would move and attack differently;
	so its ok to redefine all methods.
	"""

	current_direction = POS_UP
	previous_x = 0

	def __init__(self, enemy, player, director):
		Controller.__init__(self, enemy, director)
		self.player = player
		self.enemy_speed = 0.10
		self.ttl = 0
		self.lastSpeedX = 0
		self.lastSpeedY = 0


	def update(self, time, scene):
		"""
		Updates the state of the enemy.
		"""
		self.character.attacking = False
		collisionMap = scene.collisionBg
		self.character.speedX = 0
		self.character.speedY = 0
		self.move_behavior(time, collisionMap, scene)

		if self.check_melee_hit():
			print "%s man dao una ostia!" % self
			self.character.hp = self.character.hp - self.player.atk

		

		# Quite redundant now, but if the camera moves away from the center will still work
		self.character.atkX = self.player.rect.x + scene.camera.state.x - scene.camera.state.left
		self.character.atkY = self.player.rect.y + scene.camera.state.y - scene.camera.state.top
		
		self.attack()
		
		if self.character.equippedWpn:
			self.character.equippedWpn.update(time, self.character, scene)
			self.character.update_attack_cooldown(time)

	def attack(self):
		"""
		Makes the enemy attack when possible.
		"""

		if self.detect_player() and self.checkRaytracing_subSurface() and self.character.can_attack():
			self.character.attacking = True
		if self.collides_with_player() and self.character.can_attack():
			self.player.receive_attack(self.character.atk)

	def check_melee_hit(self):
		""" 
		Returns true when been attacked with a melee weapon.
		"""
		return self.player.is_attacking() and self.collides_with_player() and self.player.has_melee_weapon()


	def collides_with_player(self):
		""" 
		Returns true if the enemy overlaps the player.
		Note: It has a small 30 u. margin
		"""

		overlaps_y = abs(self.player.rect.y - self.character.rect.y) < 30
		overlaps_x = abs(self.player.rect.x - self.character.rect.x) < 30
		return  overlaps_x and overlaps_y


	def detect_player(self, detection_range=DETECTION_RANGE):
		""" 
		Cheacks whether the player is in range.
		"""

		delta_x = self.player.rect.x - self.character.rect.x
		delta_y = self.player.rect.y - self.character.rect.y

		distance = math.sqrt(delta_x * delta_x + delta_y * delta_y)

		return distance < detection_range

	def checkRaytracing(self):
		""" 
		Checks if the enemy sees the player. Not very efficient implementation as it processes the whole screen.
		"""

		collisionBg = self.director.scene.collisionBg
		collisionBg.set_colorkey((0,0,0))              
		collisionMap_mask = pygame.mask.from_surface(collisionBg)
		
		lineSurface = pygame.Surface((800,600))
# 		lineSurface.fill((0,0,0))
		
		pygame.draw.line(lineSurface, (255,255,255), \
                (self.player.rect.x + self.director.scene.camera.state.x, \
                 self.player.rect.y + self.director.scene.camera.state.y), \
                (self.character.rect.x + self.director.scene.camera.state.x, \
                 self.character.rect.y + self.director.scene.camera.state.y), 3)
		
# 		lineSurface.convert()
		lineSurface.set_colorkey((0,0,0))
		line_mask = pygame.mask.from_surface(lineSurface)
		overlap = line_mask.overlap(collisionMap_mask , (self.director.scene.camera.state.x, self.director.scene.camera.state.y))
# 		print overlap


		if overlap is not None:
			return False
		return True
	
	
	def checkRaytracing_subSurface(self):
		""" 
		Checks if the enemy sees the player.
		It only takes into account the region which corners are the player and the enemy.
		"""

		px = self.player.rect.x
		py = self.player.rect.y
		
		ex = self.character.rect.x
		ey = self.character.rect.y
		
		sx = ex
		sy = ey
		sw = abs(px - ex) + 1 # + 1 to keep checking it when player and enemy are on same line
		sh = abs(py - ey) + 1
		
# 		if sw == 0:
# 			sw = 1
# 		if sh == 0:
# 			sh = 1
		
# 		print "sx: " + str(sx)
# 		print "sy: " + str(sy)
# 		print "sw: " + str(sw)
# 		print "sh: " + str(sh)
		
		odd = 0
		line = [0, 0, sw, sh]
		
		if px < ex:
			sx = px
			odd += 1
		
		if py < ey:
			sy = py
			odd += 1
		
		if odd == 1:
			line = [sw, 0, 0, sh]

		collisionBg = self.director.scene.collisionBg.subsurface(pygame.Rect(sx, sy, sw, sh)).copy()
		collisionBg.set_colorkey((0,0,0))              
		collisionMap_mask = pygame.mask.from_surface(collisionBg)
		
		lineSurface = pygame.Surface((sw,sh))
# 		lineSurface.fill((0,0,0))
		
		pygame.draw.line(lineSurface, (255,255,255), (line[0], line[1]), (line[2], line[3]), 3)
		if sw == 1 or sh == 1:
			lineSurface.fill((255,255,255))
		
# 		lineSurface.convert()
		lineSurface.set_colorkey((0,0,0))
		line_mask = pygame.mask.from_surface(lineSurface)
		overlap = line_mask.overlap_area(collisionMap_mask , (0, 0))
# 		print overlap


		if overlap > 10:
			return False
		return True

	def follow_player(self, time, collisionMap):
		""" 
		Makes the enemy follow the player if the player is near.
		"""

		# Calculatelayer relative position
		delta_x = self.player.rect.x - self.character.rect.x
		delta_y = self.player.rect.y - self.character.rect.y
		distance = math.sqrt(delta_x * delta_x + delta_y * delta_y)

		# Check if the player is too far away
		if (distance > DETECTION_RANGE):
			return False


		# Detect if the player is visible using raytracing
		if not self.checkRaytracing_subSurface():
			return False



		# Move enemy
		if distance > 20:
			coef = float(self.enemy_speed) / distance

			self.character.speedX = delta_x * coef
			self.character.speedY = delta_y * coef
			self.character.attacking = False
		else:
			self.character.attacking = True


		return True


	def random_move(self, time, collisionMap):
		"""
		Generates random moves for the enemy.
		"""
		def new_random_move():
			self.ttl = random.randint(10, 100)
			self.lastSpeedX = random.gauss(0, 0.1)
			self.lastSpeedY = random.gauss(0, 0.1)
			distance = math.sqrt(self.lastSpeedX ** 2 + self.lastSpeedY ** 2)
			coef = float(self.enemy_speed) / distance
			self.lastSpeedX = self.lastSpeedX * coef
			self.lastSpeedY = self.lastSpeedY * coef

		if self.ttl == 0:
			new_random_move()
		else:
			self.ttl -= 1

		self.character.speedX = self.lastSpeedX
		self.character.speedY = self.lastSpeedY

		timesCollided = 0

		while (timesCollided < MAX_TIMES_COLLIDED) and \
		      (self.character.will_collide(time, collisionMap)):
			timesCollided += 1
			new_random_move()
			self.character.speedX = self.lastSpeedX
			self.character.speedY = self.lastSpeedY

		return True

	def avoid_enemy_overlap(self, scene):
		"""
		Modifies behavior if the enemy collides with another.
		"""
		if len(pygame.sprite.spritecollide(self.character, scene.enemyGroup, False)) > 1:
			if bool(random.getrandbits(1)):
				self.character.speedX = -self.character.speedX
				self.character.speedY = -self.character.speedY

	def move_behavior(self, time, collisionMap, scene):
		"""
		Determines how the enemy moves.
		"""
		if not self.follow_player(time, collisionMap):
			self.random_move(time, collisionMap)

		self.avoid_enemy_overlap(scene)

		self.update_pos(self.character.speedX, self.character.speedY)
		self.character.rotatePosImage(time)
		self.character.move(time, scene)