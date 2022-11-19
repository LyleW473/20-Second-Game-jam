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
enemy_image = pygame.transform.scale(enemy_image,(48,48))
staff_image = pygame.image.load('graphics/WukongStaff.png').convert_alpha()



# Variables
max_enemies = 0
generate_x_cooldown = 1000
clicked = False
click_cooldown = 1500 # 1.75 seconds
staff_count = 0
temp_mouse_position = 0
initial_staff_position_spacing = 0

def draw_background():
	screen.fill(WHITE)
	pygame.draw.rect(screen, GREEN, (0, screen_height - 80, screen_width, 80), 100)

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
		self.width = 7 * scale
		self.height = 48 * scale
		self.rect = pygame.Rect(0,0, self.width, self.height)
		self.rect.center = (x, y)
		self.rect.x = x
		self.rect.y = y
		self.position_finding = False
		self.position_reached = False
		self.on_ground = True
		self.speed_multiplier = 1

		self.initial_click_time = 0
		self.on_ground_time = 0
		self.clicked = False


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
				#self.clicked = False
				# Reset the speed multiplier
				self.speed_multiplier = 1


		# Check for collision with player
		if pygame.sprite.spritecollide(player, staff_group, True):
			# Set the staff count to 0 , allowing the player to throw another staff
			staff_count = 0
			

		# Draw the staff onto the screen
		screen.blit(self.image,(self.rect.x - 63, self.rect.y)) # self.rect.x - 63
		pygame.draw.rect(screen, BLACK, self.rect, 2)
		pygame.draw.line(screen, BLACK, (0, 300), (screen_width, 300))

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

		self.rect.y += 15
		if self.rect.y > screen_height - self.height - 80:
			self.kill()

		screen.blit(self.image, (self.rect.x - 9, self.rect.y - 6))
		pygame.draw.rect(screen, BLACK, self.rect, 2)

class Enemy_2(pygame.sprite.Sprite):
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


#delta_x = 0
#delta_y = 0 
distance_travelled_x = 0 
distance_travelled_y = 0 

# Game loop
run = True
while run:	
	# Limit frame rate to 60 
	clock.tick(60)

	# Draw + update
	draw_background()
	player.update() 

	# If there are no staffs
	if len(staff_group) > 0:
		# This variable updates the staff_count variable so that another staff can be spawned and that the previous one that was collided with disappears
		staff_count = staff.update(staff_count)



	#enemy_group.update()

	# Generate 5 enemies
	for x_num in range(1,6):
		# Initiate variable to add to x co-ordinate of enemies
		spacing = random.choice([-50,50])
		# If the length of the enemy group is less than 4, then spawn enemies
		if len(enemy_group) < 5:
			# Spawn enemy
			enemy = Enemy((x_num * 150) + spacing, - 40)
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

	#  If the mouse is clicked, find the mouse position and move the staff towards it
	if clicked == True:
		# If the staff is not already trying to find the position of the mouse
		if staff.position_finding == False:
			# Reset position reached variable
			staff.position_reached = False
			# Find the position of the mouse
			position = pygame.mouse.get_pos()
			# Set position vector
			staff.position_finding = True



	# Check if the staff is back on the ground (This is the scenario where the player has clicked and the staff is coming back to the ground)
	if staff_count > 0:
		if staff.on_ground == True and staff.clicked == True and staff.position_finding == False:
			# If 1.5 seconds have passed since the staff has landed on the ground
			if pygame.time.get_ticks() - staff.initial_click_time >= click_cooldown:
				#print(pygame.time.get_ticks())
				staff.clicked = False



	# Start moving the staff towards the clicked position
	if staff_count > 0:
		if staff.position_finding == True:	
			# The staff cannot be on the ground if we are calculating how to move the staff to the clicked position
			staff.on_ground = False

			if position[0] < staff.rect.left: # On the left side of the staff
				delta_x = staff.rect.centerx - position[0] # The difference between the x co-ordinate of the staff and the clicked position
			if position[0] > staff.rect.right: # On the right side of the staff
				delta_x = position[0] - staff.rect.centerx + 9 # Bug: the final position will never be reached without the +9, probably a floating point error
			
			# The difference between the y co-ordinate of the staff and the clicked position
			delta_y = staff.rect.centery - position[1]
			
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


			# Check if the staff is at the clicked position
			if staff.rect.centerx == position[0] and staff.rect.centery == position[1]:
				print("mouse position reached")
				distance_travelled_x =0
				distance_travelled_y = 0
				staff.position_finding = False
				staff.position_reached = True
				clicked = False
				movement_x = 0
				movement_y = 0
				delta_x = 0
				delta_y = 0




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
			# Temporary
			temp_mouse_position = pygame.mouse.get_pos()
			if temp_mouse_position[0] < player.rect.left: # If the mouse position is to the left of the player
				initial_staff_position_spacing = -100
			elif temp_mouse_position[0] > player.rect.right:
				initial_staff_position_spacing = 100

			# If there are no staffs:
			if staff_count == 0:
				#print(staff.initial_click_time)
				#clicked = True
				#staff.clicked = True
				staff = Wukong_Staff(player.rect.centerx + initial_staff_position_spacing , 777)
				staff_group.add(staff)
				staff_count = 1

			if staff.position_finding == False and staff.on_ground == True and staff.clicked == False:

				print(temp_mouse_position)
				staff.initial_click_time = pygame.time.get_ticks()
				staff.clicked = True
				clicked = True


		if event.type == pygame.MOUSEBUTTONUP and staff.position_reached == True:
			clicked = False





	pygame.display.update()


