import pygame

# Screen
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

class Ground():
	def __init__(self, x, y, surface):
		# Animations 
		self.animation_list = []
		self.animation_frame_index = 0
		self.animation_frame_displayed_time = pygame.time.get_ticks()

		for num in range(0,20):
			# Note: Ground is 200 x 40 pixels wide
			image = pygame.image.load(f'graphics/Ground/Ground{num}.png')
			self.image = pygame.transform.scale(image, (1000, 130))
			self.animation_list.append(self.image)

		# Assign animation
		self.image = self.animation_list[self.animation_frame_index]
		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 

		# Assign surface
		self.surface = surface


	def draw(self):
		animation_cooldown = 100 # 3 seconds

		# Set the image based on the animation frame index
		self.image = self.animation_list[self.animation_frame_index]

		# Check if enough time has passed since the last animation frame update
		if (pygame.time.get_ticks() - self.animation_frame_displayed_time) > animation_cooldown:
			self.animation_frame_displayed_time = pygame.time.get_ticks()
			self.animation_frame_index += 1

		# Check if the frame index is greater than the number of frames in the animation, if it is, reset the animation
		if self.animation_frame_index >= len(self.animation_list):
			self.animation_frame_index = 0		


		# Draw the background onto the screen
		self.surface.blit(self.image, (self.rect.x, self.rect.y)) 


