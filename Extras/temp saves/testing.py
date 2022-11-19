# Import modules
import pygame, sys, random, math
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

# Screen
screen_width = 1000
screen_height = 980
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


		#if self.rect.x == position[0]:
			#print(self.rect.x)
			#print(position[0])
			#self.position_reached = True
			#self.position_finding = False



			#elif self.rect.x == position
		#elif self.rect.center == position and self.position_reached == False:
			#self.position_reached = True

	def draw(self):

		# Check if staff has reached position
		#print(self.position_reached)
		#if self.position_reached == True:
		#	self.kill()


		# Draw the staff onto the screen
		screen.blit(self.image,(self.rect.x - 63, self.rect.y))
		pygame.draw.rect(screen, BLACK, self.rect, 2)



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
staff = Wukong_Staff((screen_width // 2) + 20, screen_height - 180)

# Groups
enemy_group = pygame.sprite.Group()
staff_group = pygame.sprite.Group()
staff_group.add(staff)

# Vectors

looking_vector = pygame.math.Vector2(1,1)


# Game loop
run = True
while run:	

	staff_vector = pygame.math.Vector2(staff.rect.x, staff.rect.y)
	# Limit frame rate to 60 
	clock.tick(60)

	# Draw + update
	draw_background()
	player.update() 
	staff.draw()
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


	# If the button is clicked , add more conditions later on
	if clicked == True:
		#print("clicked")
		#print(staff.position_finding)
		# If the staff is not already trying to find the position of the mouse
		if staff.position_finding == False:
			# Reset position reached variable
			staff.position_reached = False
			# Find the position of the mouse
			position = pygame.mouse.get_pos()
			# Set position vector
			mouse_vector = pygame.math.Vector2(position)
			#print(mouse_vector)
			staff.position_finding = True

				
	# Start moving the staff towards the clicked position
	if staff.position_finding == True:	
		# Find angle between player vector and mouse vector
		angle_staff_and_mouse_degree = staff_vector.angle_to(mouse_vector)
		print(angle_staff_and_mouse_degree)
		staff.position_finding = False


		#elif angle_player_and_mouse_degree > 0: # Positive
			#staff.rect.x -= abs(angle_player_and_mouse_degree // 10)
			#staff.rect.y += abs(angle_player_and_mouse_degree // 10)


	# Vectors
	mouse_pos = pygame.mouse.get_pos()
	delta = mouse_pos - staff_vector




	# Calculate angle:
	angle_to_mouse = math.atan2(delta.y, delta.x)
	looking_vector.xy = (100 * math.cos(angle_to_mouse), 100 * math.sin(angle_to_mouse))


	pygame.draw.line(screen, (255,50,50), staff_vector + (25, 25), pygame.mouse.get_pos())

	pygame.draw.line(screen, (50, 255,50), staff_vector + (25, 25), staff_vector + looking_vector)







			#if staff.rect.x == position[0] and staff.rect.y == position[1]:
				#clicked = False
				#print("mouse position reached")
				#print(clicked)
				#staff.position_finding = False
				#staff.position_reached = True




				

		#print(position)
		#print(staff.rect.x)



		

	


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

		if event.type == pygame.MOUSEBUTTONDOWN and staff.position_finding == False:
			clicked = True
		if event.type == pygame.MOUSEBUTTONUP and staff.position_reached == True:
			clicked = False





	pygame.display.update()


