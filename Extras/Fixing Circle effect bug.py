# Import modules
import pygame, sys, random, math
from decimal import Decimal
from pygame.locals import*
from enemy import Enemy
from CircleVFX import CircleEffect

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

# Staff variables

initial_staff_position_x_spacing = 0 # Used to decide where the staff will spawn
staff_count = 0 # Keeps track of how many staffs there are 
delta_x = 0 # Used to store the difference in x positions of the staffs initial spawn and the clicked mouse position
delta_y = 0 # Used to store the difference in y positions of the staffs initial spawn and the clicked mouse position
movement_x = 0 # Used to increment the value of the staff's center x
movement_y = 0 # Used to increment the value of the staff's center y
allowed_to_click = True	# Used as a limit to when the player can click for a new position
clicked = False # This variable is changed whenever a mouse click is detected


# Enemy variables
enemy_spawning_cooldown = 500 # 1 second
starting_enemy_spawned = False 



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
			self.velocity_y -= 18
			self.on_ground = False
			self.can_double_jump = True
		# Go for double jump (Only if its during the first jump)
		elif self.can_double_jump == True:
			self.velocity_y -= 18
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


		# With tiles
		# Note: Checking collisions in the x and y direction separately. This is to help avoid any bugs.
		for tile in tile_list:
			# Check for collision in the x direction
			if tile.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
			if tile.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				# Check if the player is below the tile i.e. Jumping from below and the player's head is hitting the tile
				if self.velocity_y < 0:
					dy = - (self.rect.top - tile.bottom)
					# Set the gravity to 0
					self.velocity_y = 0
				# Check if the player is above the tile i.e. Falling on top of the tile
				elif self.velocity_y >= 0:
					dy = - (self.rect.bottom - tile.top) 
					# Allow the player to jump again, since the player is on the "ground" again.
					self.on_ground = True

			
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


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# World tiles
# Notes: width = 150 except for middle tile
# Far left 
Tile1 = Rect(200 ,750, 150, 25) # (x top left, y top left, width, height) 
# Left 
Tile2 = Rect(200 ,250, 150, 25) # (x top left, y top left, width, height)
# Middle 
Tile3 = Rect(500 - (300 / 2) ,500, 300, 25) # (x top left, y top left, width, height)	
# Right
Tile4 = Rect((850 - 150),250, 150, 25) # (x top left, y top left, width, height)
# Far right 
Tile5 = Rect(850 - 150 ,750, 150, 25) # (x top left, y top left, width, height)

# List that will hold all the world tiles
tile_list = []

# Add all of the tiles created inside of a list
tile_list.append(Tile1)
tile_list.append(Tile2)
tile_list.append(Tile3)
tile_list.append(Tile4)
tile_list.append(Tile5)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Instances
player = Player((screen_width // 2), (screen_height - 80)) # y = 1000 - 80
#staff = Wukong_Staff(screen_width // 2, screen_height // 2)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Groups
staff_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
circle_effect_group = pygame.sprite.Group()

# Variables (MOVE UP LATER)



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
	# WORLD TILES

	# Draw every tile inside of the tile list
	for tile in tile_list:
		pygame.draw.rect(screen, RED, tile)

	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# ENEMIES

	enemy_group.update()


	# TEMPORARY, DRAW THE LINES OF EACH ENEMY

	#for enemy in enemy_group:
	#	pygame.draw.line(screen, RED, (enemy.rect.centerx, 0), (enemy.rect.centerx, screen_height), 2)
	#	pygame.draw.line(screen, BLUE, (0, enemy.rect.centery), (screen_width, enemy.rect.centery), 2)
	#	pygame.draw.line(screen, GREEN, (0, enemy.rect.top), (screen_width, enemy.rect.top), 2)
	#	pygame.draw.line(screen, GREEN, (0, enemy.rect.bottom), (screen_width, enemy.rect.bottom), 2)

	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Spawning enemies
	# Note: 165 is the width of the arrow image, 180 is the height of the arrow image

	# Spawn one enemy
	# Note: The starting enemy spawned variable is used to fix the bug that if the first enemy is destroyed before enough time has passed, it'll keep spawning the starting 
	# Note PT2: at the same starting position
	if len(enemy_group) < 1 and starting_enemy_spawned == False:
		# Generate a random x co-ordinate for the starting enemy to spawn at
		random_x = random.randint(25, screen_width - 25)
		# Instantiate and add the starting enemy to the enemy group
		enemy = Enemy(random_x, -180)
		enemy_group.add(enemy)
		# Set the first enemy spawned to true (bug explained inside the note)
		starting_enemy_spawned = True
		# Record the time 
		last_enemy_spawned_time = pygame.time.get_ticks()

	# Check if enough time has passed since the last enemy was spawned, if there has, then spawn another enemy
	if (pygame.time.get_ticks() - last_enemy_spawned_time) > enemy_spawning_cooldown:

		# Generate a random x co-ordinate for the enemy to spawn at. The enemy will only spawn within the screen
		random_x = random.randint(25, screen_width - 25)
		enemy = Enemy(random_x , - 180)
		# Add enemy to the group (so it can be updated)
		enemy_group.add(enemy)
		# Set the last time an enemy was spawned to now
		last_enemy_spawned_time = pygame.time.get_ticks()

	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Collision

	# Check collision for every single enemy inside the enemy group
	for enemy in enemy_group:
		# Collision with the floor
		if enemy.rect.bottom >= (screen_height - 60): # Note: I used "-60" instead of "-80" because it looks better visually)
			# Delete the enemy if it collides with the floor
			enemy.kill()

		# Only check for collisions between the staff and enemies if there is a staff spawned in the world
		if staff_count > 0:
			# First check for rect collision between the staff and enemies
			if pygame.sprite.spritecollide(staff, enemy_group, False):
				# If this occurs, look for a more accurate collision between the staff and enemies
				if pygame.sprite.spritecollide(staff, enemy_group, True, pygame.sprite.collide_mask):
					enemy.kill()
					# Circle effects
					# If there is a collision instantiate a circle effect at where the enemy died
					circle = CircleEffect(staff.rect.centerx, staff.rect.centery, 0, 2) # (x, y, radius, line thickness)
					# Note: originally we drew the circle effect at the (enemy.rect.centerx, enemy.rect.centery), drawing it at the staff makes more sense and fixes the "bug"
					circle_effect_group.add(circle)


		# First check for rect collision between the staff and enemies
		if pygame.sprite.spritecollide(player, enemy_group, False):
			# Look for a more accurate collision between the staff and enemies
			if pygame.sprite.spritecollide(player, enemy_group, True, pygame.sprite.collide_mask):
				# NOTE ADD MORE HERE E.G SOUND EFFECTS, COINS BEING REMOVED, ETC.
				pass

	# Update enemies
	enemy_group.update()
	# Update circle effects
	circle_effect_group.update()

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
			staff = Wukong_Staff(player.rect.centerx + initial_staff_position_x_spacing, (screen_height - 80) - (144 // 2) )
			# Add the staff to the staff group (Group is used for the collision checking)
			staff_group.add(staff)
			# Set staff count to 1
			staff_count = 1

		# Set the pathfinding variables to true
		staff.position_finding = True
		clicked = False
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
		if staff.position_finding == True:
			screen.blit(green_reticle_image,(cursor_position[0] - (49 * 3) , cursor_position[1] - (50 * 3))) 

	# Note: The numbers "49" and "50" are the size of half of the reticle's width and height. The number "3" is to scale the size as I scaled it earlier on in the code by 3x


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
