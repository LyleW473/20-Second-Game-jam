import pygame, random

# Screen
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
# Enemy indicator
enemy_indicator_image = pygame.image.load('graphics/EnemyIndicator.png').convert_alpha() # Image is originally 32 x 32 pixels
# enemy_indicator_image = pygame.transform.scale(enemy_indicator_image, (32 * 1.5), (32 * 1.5))


# Colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		# Animations
		self.animation_list = []
		self.animation_frame_index = 0
		self.animation_frame_displayed_time = pygame.time.get_ticks()

		# Load all the images for the animation
		for num in range(0,5):
			# Note: Image is 110 x 120 pixels
			image = pygame.image.load(f'graphics/BlueArrow/BlueArrowV2{num}.png').convert_alpha()
			self.image = pygame.transform.scale(image, (165, 180))
			self.animation_list.append(self.image)

		# Assign animation
		self.image = self.animation_list[self.animation_frame_index]
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

		# Speed
		self.speed_multiplier = 1

	def update(self):
		animation_cooldown = 90 # Milliseconds

		#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# ANIMATIONS

		# Set the image based on the animation frame index
		self.image = self.animation_list[self.animation_frame_index]

		# Check if enough time has passed since the last animation frame update
		if (pygame.time.get_ticks() - self.animation_frame_displayed_time) > animation_cooldown:
			self.animation_frame_displayed_time = pygame.time.get_ticks()
			self.animation_frame_index += 1

		# Check if the frame index is greater than the number of frames in the animation, if it is, reset the animation
		if self.animation_frame_index >= len(self.animation_list):
			self.animation_frame_index = 0	

		#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# Move down towards the bottom of the screen
		self.rect.y += 8 * self.speed_multiplier

		#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# Draw the enemy onto the screen

		#screen.blit(enemy_indicator_image, (self.rect.centerx - 16  , self.rect.centery))
		screen.blit(self.image, (self.rect.x + 2, self.rect.y)) # The plus 2 is because when I was drawing the animation, the image wasn't aligned properly
		screen.blit(enemy_indicator_image, (self.rect.centerx - 14  , 8)) # minus 14 is to make the indicator be centered with the arrow. I want the indicator to be near the top of the screen so y = 8
		
		# pygame.draw.rect(screen, BLACK, self.rect, 2)


# Note: Need to start drawing the enemy because theres no point sorting all of this out yet.
# Think of ideas for an enemy.

# I think the enemies will be an arrow (like an arrow being shot from celestials) 
#[ Yellow arrow]
# Could have another enemy which is also an arrow but a different colour (maybe blue)
# Which tracks Wukong and after 4 seconds it will disappear automatically if the player hasn't
# destroyed it themselves