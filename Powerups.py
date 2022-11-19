import pygame
#from pygame.locals import *

# Screen
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# Colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Images

#staff_elongation_powerup_image = pygame.image.load('graphics/Powerups/0.png').convert_alpha()
#score_multiplier_powerup_image = pygame.image.load('graphics/Powerups/1.png').convert_alpha()
# peach_powerup_image = pygame.image.load('graphics/Powerups/2.png').convert_alpha()

# Note: All powerup images were 33 x 32 pixels 

class LongerStaff_P(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.scale = 1.25
		image = pygame.image.load('graphics/Powerups/0.png').convert_alpha()
		self.image = pygame.transform.scale(image, (33 * self.scale, 32 * self.scale))
		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 

	def update(self): 
		# This powerup spawns on one top of the tiles

		# Draw the powerup 
		screen.blit(self.image, self.rect)
		
		#pygame.draw.rect(screen, WHITE, (self.rect), 2)

class DoubleScore_P(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.scale = 1.25
		image = pygame.image.load('graphics/Powerups/1.png').convert_alpha()
		self.image = pygame.transform.scale(image, (33 * self.scale, 32 * self.scale))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self):
		# This powerup spawns on one top of the tiles

		# Draw the powerup
		screen.blit(self.image, self.rect)

		#pygame.draw.rect(screen, WHITE, (self.rect), 2)


class Peach_P(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.scale = 1.5
		image = pygame.image.load('graphics/Powerups/2.png').convert_alpha()
		self.image = pygame.transform.scale(image, (33 * self.scale, 32 * self.scale))
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

	def update(self):
		# This powerup falls from the sky
		# Increase the y position (The peach will fall down the screen)
		self.rect.y += 5

		# Check if the peach has collided with the ground, if it was, delete the peach
		if self.rect.bottom >= (screen_height - 80):
			self.kill()



		# Draw the peach 
		screen.blit(self.image, self.rect)


class FasterMovementSpeed_P(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.scale = 1.25
		image = pygame.image.load('graphics/Powerups/3.png').convert_alpha()
		self.image = pygame.transform.scale(image, (33 * self.scale, 32 * self.scale))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self):
		# This powerup spawns on one top of the tiles

		# Draw the powerup
		screen.blit(self.image, self.rect)

		#pygame.draw.rect(screen, WHITE, (self.rect), 2)

class IncreasedStaffTravelSpeed_P(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.scale = 1.25
		image = pygame.image.load('graphics/Powerups/4.png').convert_alpha()
		self.image = pygame.transform.scale(image, (33 * self.scale, 32 * self.scale))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self):
		# This powerup spawns on one top of the tiles

		# Draw the powerup
		screen.blit(self.image, self.rect)

		#pygame.draw.rect(screen, WHITE, (self.rect), 2)


