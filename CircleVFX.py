import pygame, random
#from pygame.locals import *

# Screen
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

#transparency_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
#transparency_surface.set_alpha(255) # 255 is the default alpha value of an opaque surface

# Colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

class CircleEffect(pygame.sprite.Sprite):
	def __init__(self, x, y, radius, line_thickness):
		pygame.sprite.Sprite.__init__(self)
		self.x = x 
		self.y = y 
		self.radius = radius
		self.line_thickness = line_thickness
		self.alpha_value = 255 # 255 is the default alpha value of an opaque surface

	def update(self):
		#print(self.radius)
		# If the radius is not equal to 100
		if self.radius != 100:
			# Increment the radius until it becomes 100
			self.radius += 2
			# As the circle expands to 100, it will start to fade away
			self.alpha_value -= 5
			# Check if the alpha value has gone below 0 (because if it does, then an error will be printed out as you cannot have a negative alpha value)
			if self.alpha_value <= 0:
				# Set the alpha value limit to 0
				self.alpha_value = 0

		# If the radius is equal to 100
		if self.radius == 100:
			self.kill()

		# Create a circle rect
		circle_rect = pygame.Rect((self.x, self.y), (0,0)).inflate((self.radius * 2, self.radius * 2))	
		# Create an alpha surface for the circle
		circle_alpha_surface = pygame.Surface(circle_rect.size, pygame.SRCALPHA) # (size of the circle "rectangle", declaring pygame SRC Alpha)
		# Draw circles onto the alpha surface

		# Outer circle
		pygame.draw.circle(circle_alpha_surface, (255,255,255,self.alpha_value), (self.radius, self.radius), self.radius, self.line_thickness + 1) # (surface, (color, alphaValue), (center), radius, line thickness)
		# Inner circle
		pygame.draw.circle(circle_alpha_surface, (255,255,255,self.alpha_value), (self.radius, self.radius), self.radius - 30, self.line_thickness) # (surface, (color, alphaValue), (center), radius, line thickness)

		# Blit the surface and the circle onto the screen. (The alpha surface and the circle will be blended together)
		screen.blit(circle_alpha_surface, circle_rect)


		# Alternative method (without alpha):
		# Draw the first outer circle
		#pygame.draw.circle(transparency_surface, (0,0,0,128), (self.x, self.y), self.radius, self.line_thickness)
		# Draw the second outer circle
		#pygame.draw.circle(transparency_surface, BLACK, (self.x, self.y), self.radius - 5, self.line_thickness)
		# Draw the first inner circle
		#pygame.draw.circle(transparency_surface, BLACK, (self.x, self.y), self.radius + 30, self.line_thickness)
		# Draw the second inner circle
		#pygame.draw.circle(transparency_surface, BLACK, (self.x, self.y), self.radius - 10, self.line_thickness)




