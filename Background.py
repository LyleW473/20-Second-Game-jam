import pygame, sys

# Screen
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# Note: could remove these and instead pass them as parameters (the same way it was done with the background.draw() stuff., Same applies with ground.py

class Background():
	def __init__(self, x, y, surface):
		# Animations 
		self.animation_list = []
		self.animation_frame_index = 0
		self.animation_frame_displayed_time = pygame.time.get_ticks()

		for num in range(0,65):
			# Note: Background is 200 x 184 pixels wide
			image = pygame.image.load(f'graphics/Background/Background {num}.png').convert_alpha()
			self.image = pygame.transform.scale(image, (1000, 1000))
			self.animation_list.append(self.image)

		# Assign animation
		self.image = self.animation_list[self.animation_frame_index]
		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 

		# Assign surface
		self.surface = surface


	# Note: I separated them into two different functions because I wanted the replay menu to have a background, but not to update
	def update_animation(self):
		animation_cooldown = 3000 # 3 seconds

		# Set the image based on the animation frame index
		self.image = self.animation_list[self.animation_frame_index]

		# Check if enough time has passed since the last animation frame update
		if (pygame.time.get_ticks() - self.animation_frame_displayed_time) > animation_cooldown:
			self.animation_frame_displayed_time = pygame.time.get_ticks()
			self.animation_frame_index += 1

		# Check if the frame index is greater than the number of frames in the animation, if it is, reset the animation
		if self.animation_frame_index >= len(self.animation_list):
			self.animation_frame_index = 0		


	def draw(self):

		# Draw the background onto the screen
		self.surface.blit(self.image, (self.rect.x, self.rect.y)) 



