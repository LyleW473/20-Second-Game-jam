# Import modules
import pygame, sys, random, math
from decimal import Decimal
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

# Screen
screen_width = 1000
screen_height = 1000 # 980
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Wukong's display / bouncebackability")# Doing the themes: Rocket, Royalty, It came back (Could have a boomerang projectile that the monkey king can throw at the rockets) Try implement more themes


# Colours 
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)


# Load images
player_image = pygame.image.load('graphics/Wukong1.png').convert_alpha()
enemy_image = pygame.image.load('graphics/enemy.png').convert_alpha()
enemy_image = pygame.transform.scale(enemy_image,(48,48)).convert_alpha()
staff_image = pygame.image.load('graphics/WukongStaff.png').convert_alpha()



# VARIABLES

#-------------------------------------------------
# Enemy variables
max_enemies = 0
generate_x_cooldown = 1000

#-------------------------------------------------
# Initial staff position variables
staff_count = 0
temp_mouse_position = 0 
initial_staff_position_spacing = 0
special_initial_staff_position_spacing = 0
invalid_position = False
#-------------------------------------------------
# Staff cooldown variables
clicked = False
click_cooldown = 250 # 0.25 seconds
num_of_throws = 0
time_now = 0
on_ground_time_list = []
time_now_list = []
#-------------------------------------------------
# New staff positions calculating variables
distance_travelled_x = 0 
distance_travelled_y = 0 




def draw_background():
	screen.fill(WHITE)


class Player():
	def __init__(self, x, y):
		scale = 2
		self.image = pygame.transform.scale(player_image, (48 * scale, 48 * scale))
		self.width = 30 * scale
		self.height = 43 * scale
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x, y)


		# Movement
		self.velocity_y = 0

		# Double jump
		self.on_ground = True
		self.can_double_jump = False

		# Animation
		self.flipped_image = pygame.transform.flip(self.image, True, False)
		self.flip_image = False



	def update(self):
		dx = 0 
		dy = 0
		scale = 2


		# Horizontal movement (Vertical movement is within event handler)
		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			self.flip_image = True

			dx -= 12
		if key[pygame.K_d]:
			dx += 12
			self.flip_image = False

		# Handle gravity
		self.velocity_y += 1
		if self.velocity_y >= 10:
			self.velocity_y = 10

		dy += self.velocity_y


		# Collision

		# Check for collision with the edges of the screen
		if (self.rect.left + dx) < 0:
			dx = - self.rect.left
		if self.rect.right + dx > screen_width:
			dx = screen_width - self.rect.right



		# Check if we need to flip the player's image
		if self.flip_image == True:
			self.image = self.flipped_image
		if self.flip_image == False:
			self.image = pygame.transform.flip(self.flipped_image, True, False)


		# Update player's position
		self.rect.x += dx
		self.rect.y += dy

		# Temporary boundary bottom
		if self.rect.bottom >= screen_height - 80:
			self.rect.bottom = screen_height - 80
			self.on_ground = True
			dy = 0
		pygame.draw.line(screen, BLACK, (0, screen_height - 80), (screen_width, screen_height - 80))

		# Draw player onto screen
		screen.blit(self.image, (self.rect.x - (9 * scale) , self.rect.y - (4 * scale)))
		pygame.draw.rect(screen, BLACK, self.rect, 2)


	def jump(self):
		# Reset gravity
		self.velocity_y = 0
		# First jump
		if self.on_ground == True:
			self.velocity_y -= 15
			self.on_ground = False
			self.can_double_jump = True
		# Second jump (If the previous conditions were not True, check this condition. Because self.on_ground was false after the first jump, but self.can_double_jump was true, it can perform a consecutive jump)
		elif self.can_double_jump:
			self.velocity_y -= 15
			self.can_double_jump = False


class Wukong_Staff(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		scale = 3

		self.image = pygame.transform.scale(staff_image, (48 * scale, 48 * scale))
		self.original_image = self.image		
		self.rotating_image = pygame.transform.scale(staff_image, (48 * scale, 48 * scale))
		self.width = 7 * scale
		self.height = 48 * scale
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.center = (x, y)		
		self.position_finding = False
		self.position_reached = False
		self.on_ground = False # Flies in the air
		self.speed_multiplier = 1
		# Used to set a time delay between when the staff has landed on the ground and when the player clicks again
		self.initial_click_time = 0
		self.clicked = False
		# Used to randomize rotation
		self.angle = 0
		self.angle_decider = random.choice([-1,1])


	def rotate(self):

		if self.position_finding == True:
			# Randomly choose -1 or 1 to decide which way the staff rotates

			self.angle += 4 * self.angle_decider
			self.image = pygame.transform.rotate(self.rotating_image, self.angle)

	def update(self, staff_count):


		# Check if staff has reached position, if it has, return the staff to the bottom of the screen
		if self.position_reached == True:

			# Depending on how high the staff is, increase the fall speed
			# If the staff is above (x, 300), it will fall 2 times as fast
			if self.rect.top <= 300:
				self.speed_multiplier = 2

			self.rect.centery += 30 * self.speed_multiplier

			# If the staff has reached the ground, stop it
			if self.rect.bottom >= screen_height - 80:
				self.rect.bottom = screen_height - 80
				self.position_reached = False
				self.position_finding = False
				# Allow the player to click again
				self.on_ground = True
				#print("landed on ground")
				# Reset the speed multiplier
				self.speed_multiplier = 1


		# Draw the staff onto the screen
		screen.blit(self.image,((self.rect.x - 15, self.rect.y - 2))) # self.rect.x - 63
		pygame.draw.rect(screen, BLACK, self.rect, 2)
		pygame.draw.line(screen, BLACK, (0, 300), (screen_width, 300))

		# Update mask
		self.mask = pygame.mask.from_surface(self.image)

		return staff_count


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_image
		self.width = 30
		self.height = 30
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x, y)
		self.time_now = pygame.time.get_ticks()
		self.random_x = random.randint(0, screen_width)
		self.generated_x = False

	def update(self):

		# Make the enemy move downwards at all times
		self.rect.y += 10

		# If enemy collides with the ground, delete the enemy
		if self.rect.y > screen_height - self.height - 80:
			self.kill()

		screen.blit(self.image, (self.rect.x - 9, self.rect.y - 6))
		pygame.draw.rect(screen, BLACK, self.rect, 2)

class Enemy_2(pygame.sprite.Sprite): # "Heat-seeking" enemy
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		pass

	def update(self):

		# Find player's current position
		player_position_x = player.rect.x 
		player_position_y = player.rect.y
		player_position = player.rect.center

		if self.rect.center != player_position:
			# Travel towards the player's x position
			if player_position_x > self.rect.x: # The player is to the right of the enemy
				self.rect.x += 5
			if player_position_x < self.rect.x: # The player is to the right of the enemy
				self.rect.x -= 1
			# Travel towards the player's y position
			if player_position_y > self.rect.y: # The player is underneath the enemy
				self.rect.y += 1

		# Add a timer to make the projectile disappear if a few seconds have passed since its been created

# Instances
player = Player((screen_width // 2), (screen_height - 80))

# Starting staff
#staff = Wukong_Staff((screen_width // 2) + 20, screen_height - 235) # y = screen_height - 180, y = screen_height - 224

# Groups
enemy_group = pygame.sprite.Group()
staff_group = pygame.sprite.Group()

#staff_group.add(staff)

one_position_list = [0]
temp = 150


# Game loop
run = True
while run:	
	# Limit frame rate to 60 
	clock.tick(60)

	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	# Draw + update

	draw_background()
	player.update() 

	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# ENEMIES
	enemy_group.update()

	# Generate 5 enemies (OLD VERSION)
	#for x_num in range(1,6):
	#	# Initiate variable to add to x co-ordinate of enemies
	#	spacing = random.choice([-50,50])
	#	# If the length of the enemy group is less than 4, then spawn enemies
	#	if len(enemy_group) < 5:
	#		# Spawn enemy
	#		enemy = Enemy((x_num * 200) + spacing, - 40)
	#		enemy_group.add(enemy)

	# Generate 5 enemies (NEW VERSION)
	for enemy in range(1,6):
		spacing = random.choice([-50,50])
		random_x = random.randint(0,screen_width - 40)
		if len(enemy_group) < 5:
			enemy = Enemy(random_x + spacing,  - 40)
			enemy_group.add(enemy)

	# Check each enemy and update the position based on the random x co-ordinate that was generated upon instantiation
	for enemy in enemy_group:
		x = enemy.random_x
		if enemy.rect.x != x:
			if x > enemy.rect.x: # The x co-ord is to the right of the enemy
				enemy.rect.x += 1
			if x < enemy.rect.x: # The x co-ord is to the left of the enemy
				enemy.rect.x -= 1

	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# STAFF



	# If there are no staffs
	if len(staff_group) > 0:
		# This variable updates the staff_count variable so that another staff can be spawned and that the previous one that was collided with disappears
		staff_count = staff.update(staff_count)

	

	#  If the mouse is clicked, find the mouse position and move the staff towards it
	if clicked == True:
		# Don't record the time if the number of throws is 0 (i.e. the first throw)

		if staff_count == 0:
			# If this is the first throw, create a new staff and allow for the staff to start moving towards a given position
			if num_of_throws == 0:

				# Find position of mouse
				position = pygame.mouse.get_pos()	

				# Add it into a list to check the position that was clicked
				one_position_list[0] = position
				#print("one_position_list[0] = ",one_position_list[0])

				# Check whether the y position is valid or not

				# Below ground or the exact pixel of the ground
				if one_position_list[0][1] >= (screen_height - 80):
					print(one_position_list[0][1], "Invalid y position")

					invalid_position = True
					# Exit the loop
					clicked = False
					#staff.position_finding = False
					#staff.position_reached = False

				# Above ground
				if one_position_list[0][1] < (screen_height -80):
					print(one_position_list[0][1], "Valid y position")
					invalid_position = False
					# set the y co-ordinate as the screen_height - height of the staff
					staff = Wukong_Staff(player.rect.centerx + initial_staff_position_spacing , screen_height - 144 - 80) 
					staff_group.add(staff)

					staff_count = 1
					staff.clicked = True

					staff.position_finding = True
					staff.position_reached = False


		# If its past the first throw
		if num_of_throws > 0:
			if len(time_now_list) == 0: 
				# Record the time of the first click
				time_now = pygame.time.get_ticks()

			# Check if enough time has passed since the staff has landed on the ground
			if len(on_ground_time_list) > 0:  # If there is an item in this list, that means the staff has landed on the ground
				# If enough time has passed i.e. the cooldown:

				if time_now - on_ground_time_list[0] > click_cooldown:
					# Record the time_now in a list
					time_now_list.append(time_now)

					# Reset the lists, allowing for new times to be recorded
					time_now_list = []
					on_ground_time_list = []

					staff.position_finding = True
					staff.position_reached = False
					# Find position of mouse
					position = pygame.mouse.get_pos()


				else:
					pass
					#print("Not enough time has passed")



	# Check if the staff is back on the ground (This is the scenario where the player has clicked and the staff is coming back to the ground)
	if staff_count > 0:

################################################		
		# Help visualise the boundaries to where I can spawn the staff
		pygame.draw.line(screen, BLACK, (0, staff.rect.y), (screen_width, staff.rect.y))
################################################


		if staff.on_ground == True and staff.clicked == True and staff.position_finding == False:
			# If 1.5 seconds have passed since the staff has landed on the ground
			on_ground_time = pygame.time.get_ticks()
			# Record only one point in time
			if len(on_ground_time_list) == 0:
				on_ground_time_list.append(on_ground_time)
				#print("on_ground_time_list =", on_ground_time_list)

	# Start moving the staff towards the clicked position
	if staff_count > 0:

		# Start finding the position of the mouse
		if staff.position_finding == True:		

			# Checking X - position
			if position[0] < staff.rect.centerx: # On the left side of the centre staff
				delta_x = staff.rect.centerx - position[0] # The difference between the x co-ordinate of the staff and the clicked position
			if position[0] > staff.rect.centerx: # On the right side of the centre of the staff
				delta_x = position[0] - staff.rect.centerx + 9 # Bug: the final position will never be reached without the +9, probably a floating point error
			elif position[0] == staff.rect.centerx: # There is no difference in the x positions
				delta_x = 0

			
			# Checking Y - position
			# The difference between the y co-ordinate of the staff and the clicked position
			# Upwards

			print("staff.rect.centery = ", staff.rect.centery)
			# if the clicked position is above the staff 
			if position[1] < staff.rect.centery:
				delta_y = staff.rect.centery - position[1]

			# If the clicked position is below the staff
			if position[1] >=  staff.rect.centery:
				print("position[1] = ", position[1])
				delta_y = 0

				# Stops rotating and finding a new position. Sets the staff to stand on the ground
				staff.position_finding = False
				staff.rect.bottom = screen_height - 80
				clicked = False

				#staff.rect.centery = int(position[1])
				#staff.rect.centery = int(position[1])
				print(position[1])
				print(staff.rect.centery)

				#distance_travelled_x = 0
				#distance_travelled_y = 0
				#staff.position_finding = False
				#staff.position_reached = False
				#clicked = False
				#position =
				#staff_count = 0
				#num_of_throws = 0


			#elif position[1] > staff.rect.centery:
			#	print(position[1],"invalid")
			#	delta_y = 0
			#	# Ignore the mouse position, exit the loop
			#	staff.position_finding = False
			#	clicked = False


			# Y - position pathfinding

			# Moving upwards , delta_y would be a negative
			if distance_travelled_y != delta_y:
				movement_y = float(delta_y / 10) 
				if staff.rect.centery > position[1]: # Staff is below the clicked position
					# Increment the staff's y position up
					staff.rect.centery -= movement_y 
					distance_travelled_y -= movement_y


			# X - position pathfinding

			if distance_travelled_x != delta_x:
				movement_x = float(delta_x / 10)
				if staff.rect.centerx < position[0]: # The position we are looking for is to the right of the player
					staff.rect.centerx += movement_x
					distance_travelled_x += movement_x
				elif staff.rect.centerx > position[0]: # The position we are looking for is to the left of the player
					staff.rect.centerx -= movement_x
					distance_travelled_x -= movement_x


			# Rotate the staff when moving to clicked position
			staff.rotate()


			# Check if the staff is at the clicked position
			if staff.rect.centerx == position[0] and staff.rect.centery == position[1]:
				#print("mouse position reached")
				distance_travelled_x = 0
				distance_travelled_y = 0
				staff.position_finding = False
				staff.position_reached = True
				clicked = False
				movement_x = 0
				movement_y = 0
				delta_x = 0
				delta_y = 0
				num_of_throws += 1
				position = 0
				print("num_of_throws = ", num_of_throws)

	# Check for collision with enemies
	if staff_count > 0:
		# If the enemy collides with a staff, delete the enemy
		if pygame.sprite.spritecollide(staff, enemy_group, False):
			# Look for a more accurate collision between the staff and enemies, delete the enemy if there is
			if pygame.sprite.spritecollide(staff, enemy_group, True, pygame.sprite.collide_mask):
				pass

	# Check for collision with player
	if staff_count > 0:
		# Check for rect collision between the staff and the player
		if pygame.sprite.spritecollide(player, staff_group, False):
			# Look for a more accurate collision between the staff and the player
			if pygame.sprite.spritecollide(player, staff_group, True, pygame.sprite.collide_mask):
				# Reset all staff variables
				distance_travelled_x = 0
				distance_travelled_y = 0
				staff.position_finding = False
				staff.position_reached = False
				position = 0
				clicked = False
				staff_count = 0
				num_of_throws = 0

	# Draw the ground rectangle
	pygame.draw.rect(screen, GREEN, (0, screen_width - 80, screen_height, 80), 100)

	

	for event in pygame.event.get():
		if event.type == QUIT:
			run = False
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == K_SPACE:
				if player.on_ground == True:
					player.jump()
				elif player.can_double_jump == True:
					player.jump()

		if event.type == pygame.MOUSEBUTTONDOWN: #and staff.position_finding == False and staff.on_ground == True and staff.clicked == False:
			# Set the clicked variable to True
			clicked = True

			# Check where to spawn the staff based on where is clicked
			temp_mouse_position = pygame.mouse.get_pos()
			if temp_mouse_position[0] <= player.rect.left: # If the mouse x position is to the left of the player
				initial_staff_position_spacing = -100
				#invalid_position = False
			elif temp_mouse_position[0] >= player.rect.right: # If the mouse x position is to the right of the player
				initial_staff_position_spacing = 100
				#invalid_position = False

			if temp_mouse_position[1] >= screen_height - 80: # If the mouse y position is below or equal to the ground:
				pass
				#invalid_position = True

		# Reset one_position_list
		one_position_list = [0]


#			if staff_count > 0 :
#				# Record the time and set clicked to true
#				if staff.position_finding == False and staff.on_ground == True:
#						print("here",temp_mouse_position)
#						staff.initial_click_time = pygame.time.get_ticks()
#						staff.clicked = True
#						clicked = True			


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# OBSOLETE CODE
		#	# If the mouse x position is in between the player's left and player's right, i.e. is above the player
		#	elif temp_mouse_position[0] > player.rect.left and temp_mouse_position[0] < player.rect.right:
		#		print("Special")
		#		initial_staff_position_spacing = 0
		#		special_initial_staff_position_spacing = 100


		#if event.type == pygame.MOUSEBUTTONUP:
		#	# Check if there are any staffs
		#	if staff_count > 0:
		#		# Once the staff has reached the position, the click variable will be reset
		#		if staff.position_reached == True:
		#			clicked = False





	pygame.display.update()


