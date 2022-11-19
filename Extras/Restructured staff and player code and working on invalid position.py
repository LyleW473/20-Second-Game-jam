# Import modules
import pygame, sys, random, math
from decimal import Decimal
from pygame.locals import*

pygame.init()
clock = pygame.time.Clock()

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
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LOAD IMAGES
player_image = pygame.image.load('graphics/Wukong1.png').convert_alpha()
staff_image = pygame.image.load('graphics/WukongStaff.png').convert_alpha()
red_reticle_image = pygame.image.load('graphics/RedReticleV2.png').convert_alpha()
green_reticle_image = pygame.image.load('graphics/GreenReticleV2.png').convert_alpha()


red_reticle_image = pygame.transform.scale(red_reticle_image, (300,300))
green_reticle_image = pygame.transform.scale(green_reticle_image, (300,300))

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# GAME VARIABLES
clicked = False


def draw_background():
	screen.fill(WHITE)


class Player():
	def __init__(self, x, y):
		self.scale = 2
		self.image = pygame.transform.scale(player_image, (48 * self.scale, 48 * self.scale))
		self.width = 30 * self.scale
		self.height = 43 * self.scale
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x , y)

		# Movement 
		self.velocity_y = 0
		self.on_ground = True
		self.can_double_jump = False

		# Flip image
		self.flipped_image = pygame.transform.flip(self.image, True, False) # Flip the image in the x direction
		self.flip_image = False

	def jump(self):
		# Reset gravity 
		self.velocity_y = 0
		# First jump (Only if its the first jump do this)
		if self.on_ground == True:
			self.velocity_y -= 15
			self.on_ground = False
			self.can_double_jump = True
		# Go for double jump (Only if its during the first jump)
		elif self.can_double_jump == True:
			self.velocity_y -= 15
			self.can_double_jump = False


	def update(self):
		dx = 0
		dy = 0
		#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# Horizontal movement
		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			self.flip_image = True
			dx -= 12

		if key[pygame.K_d]:
			dx += 12
			self.flip_image = False

		# Vertical movement
		# Handle gravity 
		self.velocity_y += 1
		if self.velocity_y >= 10:
			# Limit gravity
			self.velocity_y = 10

		dy += self.velocity_y


		#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# Check if we need to flip the player's image

		# When moving left
		if self.flip_image == True:
			self.image = self.flipped_image
		# When moving right
		if self.flip_image == False:
			self.image = pygame.transform.flip(self.flipped_image, True, False) 

		#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# Check for collision

		# With edges of the screen
		if self.rect.right + dx > screen_width:
			dx = screen_width - self.rect.right
		if self.rect.left + dx < 0:
			dx = - self.rect.left


		# Update player's position
		self.rect.x += dx
		self.rect.y += dy

		# With bottom of the screen
		if self.rect.bottom >= screen_height - 80:
			self.rect.bottom = screen_height - 80
			self.on_ground = True
			# Note: Not sure what the point of including dy = 0 is
			#dy = 0

		#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

		# Draw player onto screen
		screen.blit(self.image, (self.rect.x - (9 * self.scale) , self.rect.y - (4 * self.scale)))
		pygame.draw.rect(screen, BLACK, self.rect, 2)


class Wukong_Staff(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.scale = 3 # Used to control the size of the object 
		self.image = pygame.transform.scale(staff_image, (48 * self.scale, 48 * self.scale))

		self.width = 7 * self.scale
		self.height = 48 * self.scale
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		# Pathfinding algorithm variables
		self.position_finding = False
		self.position_reached = False


		# Speed multiplier variable
		self.speed_multiplier = 1

		# Rotation variables
		self.image_copy = self.image
		self.angle = 0 
		self.angle_decider = random.choice([-1, 1])

	def update(self, allowed_to_click):


		# Pathfinding - related


		# Check if the staff has reached the position that was clicked
		if self.position_reached == True:
			self.rect.y += 30 * self.speed_multiplier


		# Check if the staff has reached the ground, if it has stop the staff from moving below the ground
		if self.rect.bottom >= screen_height - 80:
			self.rect.bottom = screen_height - 80
			# Reset these variables. Players are not allowed to click for a new position until the staff has landed back onto the ground
			self.position_reached = False
			allowed_to_click = True
			# Reset speed multiplier, as the staff has now reached the ground
			self.speed_multiplier = 1
			# Reset the angle to 0. This is so that when the staff is thrown again it'll start spinning
			self.angle = 0

		# Rotate staff while pathfinding
		if self.position_finding == True:
			# Randomly choose -1 or 1 to decide which way the staff rotates
			# This check is to ensure that the staff "always" lands on the base of the staff
			if abs(self.angle) != 360:
				self.angle += 20
				self.image_copy = pygame.transform.rotate(self.image, self.angle)
				



		#print(self.angle)
		#self.angle = 0



		# Speed of fall effect
		if self.rect.centery <= 300: # i.e 300 pixels from the top of the screen
			self.speed_multiplier = 2



		# Draw the staff onto the screen
		# Note: I want the staff to be drawn in the center of the rectangle and for centered rotations, I must minus half of the width and height.
		screen.blit(self.image_copy, (self.rect.centerx - int(self.image_copy.get_width() / 2) , self.rect.centery - int(self.image_copy.get_height() / 2))) 

		# Draw lines in the center x and y of the staff
		pygame.draw.line(screen, BLACK, (0, self.rect.centery), (screen_width, self.rect.centery))
		pygame.draw.line(screen, BLACK, (self.rect.centerx, 0), (self.rect.centerx, screen_height))
		pygame.draw.rect(screen, BLACK, self.rect, 2)	

		# Update mask
		self.mask = pygame.mask.from_surface(self.image)

		return allowed_to_click





initial_staff_position_x_spacing = 0 # Used to decide where the staff will spawn
staff_count = 0 # Keeps track of how many staffs there are 
delta_x = 0 # Used to store the difference in x positions of the staffs initial spawn and the clicked mouse position
delta_y = 0 # Used to store the difference in y positions of the staffs initial spawn and the clicked mouse position
movement_x = 0 # Used to increment the value of the staff's center x
movement_y = 0 # Used to increment the value of the staff's center y
allowed_to_click = True	# Used as a limit to when the player can click for a new position
invalid_position = False

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Instances
player = Player((screen_width // 2), (screen_height - 80)) # y = 1000 - 80
#staff = Wukong_Staff(screen_width // 2, screen_height // 2)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Groups
staff_group = pygame.sprite.Group()



# GAME LOOP

run = True
while run:
	clock.tick(60)
	draw_background()
	player.update()



	# Draw player and its center points
	pygame.draw.line(screen, RED, (player.rect.centerx, player.rect.centery), (player.rect.centerx, 0), 5)
	pygame.draw.line(screen, BLUE, (0, player.rect.centery), (screen_width, player.rect.centery), 5)


	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Mouse position finding
	#mouse_click_position = pygame.mouse.get_pos()

	# If the mouse button has been clicked
	if clicked == True:

		# Don't allow the player to click for a new position
		allowed_to_click = False
		mouse_click_position = pygame.mouse.get_pos()
		screen.blit(green_reticle_image, cursor_position)
		print(mouse_click_position)	

		# Check where the clicked mouse position is

		# Check y co-ord of clicked mouse position
		if mouse_click_position[1] >= (screen_height - 80): # Equal or less than the ground
			invalid_position = True


		# Check x co-ord of clicked mouse position
		if mouse_click_position[0] <= player.rect.left: # To the left of the player
			initial_staff_position_x_spacing = - ( (player.rect.width // 2) + 15 )
		if mouse_click_position[0] >= player.rect.right: # To the right of the player
			initial_staff_position_x_spacing = (player.rect.width // 2) + 15
		# If in between the player, do not spawn the staff (No need to write anything here)


		# If there are no staffs, spawn a staff
		if staff_count == 0:
			# Based on whether the mouse click position was on the left or right of the player, spawn it on the left or right of the player
			# Note: 144 // 2 = (staff.height // 2)
			if invalid_position == False:
				staff = Wukong_Staff(player.rect.centerx + initial_staff_position_x_spacing, (screen_height - 80) - (144 // 2) )
				# Add the staff to the staff group (Group is used for the collision checking)
				staff_group.add(staff)
				# Set staff count to 1
				staff_count = 1

		# Set the pathfinding variables to true
		staff.position_finding = True
		clicked = False
		invalid_position = False
		# Now we have only found a single mouse position (where the mouse was clicked), so clicked can be reset to False.
		
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


	# Pathfinding algorithm
	if staff_count > 0:
		#print(mouse_click_position)

		# use the position clicked and start travelling to the co-ordinate	
		if staff.position_finding == True:
			# Check the X - position of the position clicked
			if mouse_click_position[0] < staff.rect.centerx: # On the left side of the centre staff
				delta_x = staff.rect.centerx - mouse_click_position[0] # The difference between the x co-ordinate of the staff and the clicked position
			if mouse_click_position[0] > staff.rect.centerx: # On the right side of the centre of the staff
				delta_x = mouse_click_position[0] - staff.rect.centerx + 9 # Bug: the final position will never be reached without the +9, probably a floating point error
			elif mouse_click_position[0] == staff.rect.centerx: # There is no difference in the x positions
				delta_x = 0


			# Check the Y - position of the position clicked

			if mouse_click_position[1] < staff.rect.centery: # if the clicked position is above the staff 
				delta_y = staff.rect.centery - mouse_click_position[1]

			if mouse_click_position[1] >=  staff.rect.centery: # If the clicked position is below the staff
				delta_y = 0

			# Y - position pathfinding
			# Moving upwards , delta_y would be a negative
			movement_y = float(delta_y / 6) 
			if staff.rect.centery > mouse_click_position[1]: # Staff is below the clicked position
				# Increment the staff's y position up
				staff.rect.centery -= movement_y 

			# X - position pathfinding
			movement_x = float(delta_x / 6)
			if staff.rect.centerx < mouse_click_position[0]: # The position we are looking for is to the right of the player
				staff.rect.centerx += movement_x
			elif staff.rect.centerx > mouse_click_position[0]: # The position we are looking for is to the left of the player
				staff.rect.centerx -= movement_x


			# Check if the staff is at the clicked position
			if staff.rect.centerx == mouse_click_position[0] and staff.rect.centery == mouse_click_position[1]:
				#print("At position")

				# Set variables to correct values
				staff.position_finding = False
				staff.position_reached = True
				# Note: delta_x and delta_y get changed whenever a new click position is being found so no need to reset here

		# Return the allowed_to_click variable to the rest of the program (This is changed when the staff lands back on the ground)
		# Note: This must be outside the pathfinding algorithm
		allowed_to_click = staff.update(allowed_to_click)


		# Check for collision between the player and the staff
		# First check for rect collision between the staff and the player
		if pygame.sprite.spritecollide(player, staff_group, False):
			# Look for a more accurate collision between the staff and the player
			if pygame.sprite.spritecollide(player, staff_group, True, pygame.sprite.collide_mask):
				# Set the number of staffs back to 0
				staff_count = 0

				# In the case that the player picks up the staff whilst the staff is mid-air, allow the player to click (as the only other way it is returned is if the staff lands on the ground)
				allowed_to_click = True


	# Draw ground, it is all the way down here because I want the ground to be drawn other the staff

	pygame.draw.rect(screen, GREEN, (0, screen_width - 80, screen_height, 80), 100)
	pygame.draw.line(screen, BLACK, (0, screen_height - 80), (screen_width, screen_height - 80))


	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Draw red cursor
	pygame.mouse.set_visible(False)	
	cursor_position = pygame.mouse.get_pos()
	screen.blit(red_reticle_image, (cursor_position[0] - (49 * 3) , cursor_position[1] - (50 * 3)))

	if staff_count > 0:
		# Draw the green cursor when we are finding a new position
		if staff.position_finding == True and invalid_position == False:
			screen.blit(green_reticle_image,(cursor_position[0] - (49 * 3) , cursor_position[1] - (50 * 3)))




	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# EVENT HANDLER

	for event in pygame.event.get():
		if event.type == QUIT:
			run = False
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == K_SPACE:
				# Handle jumping
				if player.on_ground == True:
					player.jump()
				elif player.can_double_jump == True:
					player.jump()
		if event.type == pygame.MOUSEBUTTONDOWN and allowed_to_click == True:
			# Set the clicked variable to true - This allows for the mouse position to be found
			clicked = True



	pygame.display.update()
