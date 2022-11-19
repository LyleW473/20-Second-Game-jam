# Import modules
import pygame, sys, random, os
from pygame.locals import*
from enemy import Enemy
from CircleVFX import CircleEffect
from Background import Background
from Ground import Ground
from Powerups import LongerStaff_P, DoubleScore_P, Peach_P, FasterMovementSpeed_P, IncreasedStaffTravelSpeed_P
from Menus import MainMenu
from pygame import mixer

# Sounds

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()


clock = pygame.time.Clock()
countdown_time = pygame.time.get_ticks() # Need to change this to an attribute of the play button


# Set title of the game
pygame.display.set_caption('Invincible Monkey')

# Screen
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))


# Game over surface 
# Note: This is to create a slightly faded background
faded_surface = pygame.Surface((screen_width, screen_height))
faded_surface.set_alpha(90)


# Colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
GOLD = (255,223,0) 
countdown_colour = (75,0,130)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Fonts
combo_font = pygame.font.SysFont('Bahnschrift', 30)
score_font = pygame.font.SysFont('Bahnschrift',20)
countdown_font = pygame.font.SysFont('Bahnschrift', 150)
combo_font = pygame.font.SysFont('Bahnschrift', 30)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LOAD IMAGES
staff_image = pygame.image.load('graphics/WukongStaff.png').convert_alpha()
red_reticle_image = pygame.image.load('graphics/Reticle/RedReticleV3.png').convert_alpha()
green_reticle_image = pygame.image.load('graphics/Reticle/GreenReticleV3.png').convert_alpha()


red_reticle_image = pygame.transform.scale(red_reticle_image, (300,300))
green_reticle_image = pygame.transform.scale(green_reticle_image, (300,300))

increased_staff_travel_speed_status_icon_image = pygame.image.load('graphics/Powerups/4.png').convert_alpha()
faster_movement_speed_status_icon_image = pygame.image.load('graphics/Powerups/3.png').convert_alpha()
peach_status_icon_image = pygame.image.load('graphics/Powerups/2.png').convert_alpha()
double_score_status_icon_image = pygame.image.load('graphics/Powerups/1.png').convert_alpha()
longer_staff_status_icon_image = pygame.image.load('graphics/Powerups/0.png').convert_alpha()


small_world_tile = pygame.image.load('graphics/WorldTiles/small_world_tile.png').convert()
medium_world_tile = pygame.image.load('graphics/WorldTiles/medium_world_tile.png').convert()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LOAD SOUNDS
powerup_sound = pygame.mixer.Sound('sounds/Powerup.mp3')
staff_sound = pygame.mixer.Sound('sounds/staff.mp3')
enemy_destroyed_sound = pygame.mixer.Sound('sounds/enemy_destroyed.mp3')

# Change volumes
enemy_destroyed_sound.set_volume(0.5)
	
# Load main music
pygame.mixer.music.load('sounds/MainSong.mp3')
pygame.mixer.music.set_volume(0.025)
pygame.mixer.music.play(loops = -1)



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# GAME VARIABLES


amount_of_time = 20000 # Milliseconds  # Original = 20000 milliseconds



# Staff variables

initial_staff_position_x_spacing = 0 # Used to decide where the staff will spawn
staff_count = 0 # Keeps track of how many staffs there are 
delta_x = 0 # Used to store the difference in x positions of the staffs initial spawn and the clicked mouse position
delta_y = 0 # Used to store the difference in y positions of the staffs initial spawn and the clicked mouse position
movement_x = 0 # Used to increment the value of the staff's center x
movement_y = 0 # Used to increment the value of the staff's center y
allowed_to_click = False # Used as a limit to when the player can click for a new position
clicked = False # This variable is changed whenever a mouse click is detected


# Enemy variables
enemy_spawning_cooldown = 500 # 0.5 seconds
starting_enemy_spawned = False 

# Score variables
total_score = 0 # Total score displayed
score_add = 10 # This is multiplied by staff.combo_multiplier so it goes +5, +10, +20, +40
score_subtract = 10 # This is the score taken away from the player when it gets hit by an arrow
# staff.combo_multiplier # I'd rather make combo an attribute of staff rather than make it a global variable

# Powerups variables

# Lists for powerups

# A list containing all the possible spawning locations for the collectible powerups
# Note: X co-ord: location + width of rect) - (half of the width of powerup) Y co-ord = location - height of the powerup
possible_spawning_locations = [[275 - (41.25 // 2) , 710], [275 - (41.25 // 2) , 210], [500 - (41.25 // 2), 460], [775 - (41.25 // 2), 210], [775 - (41.25 // 2), 710]]
random_index_list =  [0,1,2,3,4] # A random index is chosen from here to decide where to spawn the collectible powerups
num_of_collectible_powerups = 0 # Contains the number of collectible powerups spawned

# Peach
game_started_time_peach = pygame.time.get_ticks() # Use this to find out when the game started, used for the peach spawning
peach_spawning_cooldown = 8000 # 8 seconds
# player.peach_status # Is updated whenever a collision between the peach and player is detected

# Collectible powerups:
game_started_time_collectible_powerups = pygame.time.get_ticks() # First 4 second check, this is up here because it applies to all collectible powerups that are spawned on the tiles
collectible_powerups_spawning_cooldown = 4000 
# Double Score
#player.double_score_powerup_multiplier = 1 # When the double score powerup is picked up, this will change to 2

# Faster movement speed

# Increased staff travel speed 

	

def draw_text(text, font, text_colour, x, y):
	image = font.render(text, True, text_colour)
	screen.blit(image, (x,y))

def draw_alpha_text(text, font, text_colour,  x, y):
	alpha_text = font.render(text, True ,text_colour)
	alpha_text.set_alpha(30)
	screen.blit(alpha_text,(x,y))


def reset_level(staff_count, player, allowed_to_click, amount_of_time, total_score, game_started_time_peach, game_started_time_collectible_powerups, num_of_collectible_powerups, random_index_list, starting_enemy_spawned):
	# Staff 
	for staff in staff_group:
		staff.kill()
	staff_count = 0

	# Player (Delete the old instance and create a new one)
	player.kill()
	player = Player((screen_width // 2), (screen_height - 80))

	# Core game
	allowed_to_click = False
	amount_of_time = 20000
	total_score = 0

	# Reset all spawning times
	game_started_time_peach = pygame.time.get_ticks()
	game_started_time_collectible_powerups = pygame.time.get_ticks()

	# Spawning
	num_of_collectible_powerups = 0
	random_index_list = [0,1,2,3,4]
	starting_enemy_spawned = False


	return staff_count, player,  allowed_to_click, amount_of_time, total_score, game_started_time_peach, game_started_time_collectible_powerups, num_of_collectible_powerups, random_index_list, starting_enemy_spawned


# Check for a file with a score in it
if os.path.exists('score.txt'):
	# Read the contents of the file
	with open('score.txt', 'r') as file:
		# Set the file contents into an integer and save it into the variable high score
		high_score = int(file.read())
# If there is no file with score in it, just set high score to be 0.
else:
	high_score = 0




class TextEffect(pygame.sprite.Sprite):
	def __init__(self, x , y, text, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = combo_font.render(text, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.text_displayed_time = pygame.time.get_ticks()

	def update(self):
		# Move the text up the screen
		self.rect.y -= 1
		# Check if the text has been displayed for long enough
		if (pygame.time.get_ticks() - self.text_displayed_time) > 1000:
			self.kill()


class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.scale = 3.5
		# Animations	
		self.animation_frames_list = [] # List that will contain another list, which contains animation frames with its action
		self.frame_index = 0
		self.animation_update_time = pygame.time.get_ticks() # Used to store the time when the first frame has been played
		self.action = 0 # Used to define what action the player is currently doing. 0 = Idle, 1 = Jumping , 2 = Running
		# Idle animation
		temporary_list = [] # Create a temporary list to hold the idle animation frames
		for num in range(0,12): # 12 images
			image = pygame.transform.scale(pygame.image.load(f'graphics/Player/Idle/{num}.png'), (32 * self.scale, 32 * self.scale))
			image = pygame.transform.scale(image, (32 * self.scale , 32 * self.scale))
			# Hold the image within a temporary list
			temporary_list.append(image)
		# Add it to the overall frames list
		self.animation_frames_list.append(temporary_list)

		# Jump animation
		temporary_list = [] # Create a temporary list to hold the jump animation frames
		for num in range(0,4): # 4 images
			image = pygame.transform.scale(pygame.image.load(f'graphics/Player/Jump/{num}.png'), (32 * self.scale, 32 * self.scale))
			# Hold the image within a temporary list
			temporary_list.append(image)
		# Add it to the overall frames list
		self.animation_frames_list.append(temporary_list)

		# Run animation
		temporary_list = [] # Create a temporary list to hold the run animation frames
		for num in range(0,5): # 5 images
			image = pygame.transform.scale(pygame.image.load(f'graphics/Player/Run/{num}.png'), (32 * self.scale, 32 * self.scale))
			# Hold the image within a temporary list
			temporary_list.append(image)
		# Add it to the overall frames list
		self.animation_frames_list.append(temporary_list)


		self.image = self.animation_frames_list[self.action][self.frame_index] # This will bring up the idle animation, and the first image in it
		self.width =  20 * self.scale #17 * self.scale
		self.height = 32 * self.scale
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x , y)

		# Movement 
		self.velocity_y = 0
		self.on_ground = True
		self.can_double_jump = False


		# Flip image
		self.flip_image = False

		# Powerups
		self.in_menu_time = 0 # Used to add onto the powerup timers so that when the player pauses the game, the powerup timer stays as it was prior to opening the paused menu
		# Peach
		self.peach_status = False
		self.peach_amount_of_time = 0 # Holds the amount of time left of the peach powerup
		self.peach_picked_up_time = 0 # Holds the time that the peach powerup was picked up


		# Double score
		self.double_score_status = False
		self.double_score_powerup_amount_of_time = 0 # Holds the amount of time left of the peach powerup
		self.double_score_powerup_picked_up_time = 0 # Holds the time that the peach powerup was picked up
		self.double_score_powerup_multiplier = 1


		# Faster movement speed
		self.faster_movement_speed_status = False
		self.faster_movement_speed_powerup_amount_of_time = 0  # Holds the amount of time left of the peach powerup
		self.faster_movement_speed_powerup_picked_up_time = 0	
		self.speed_multiplier = 1


		#self.longer_staff_status = False # Might need to put this into the staff so I can change the properties of the staff

	def update_animation(self):
		# Cooldowns for each animation type
		idle_animation_frame_cooldown = 150
		jump_animation_frame_cooldown = 100
		run_animation_frame_cooldown = 80

		# Set the image as the image inside the animation frame list
		self.image = self.animation_frames_list[self.action][self.frame_index]

		# Update the animation frame as long as the cooldown has passed  

		# Idle animation
		if self.action == 0 :
			# Increase the frame index if the cooldown has passed
			if pygame.time.get_ticks() - self.animation_update_time > idle_animation_frame_cooldown:
				self.animation_update_time = pygame.time.get_ticks()
				self.frame_index += 1
			# Check for if the idle animation has reached the end of its animation
			if self.frame_index >= len(self.animation_frames_list[self.action]):
				# Reset the animation (i.e. loop it)
				self.frame_index = 0

		# Jump animation
		if self.action == 1:
			# Increase the frame index if the cooldown has passed
			if pygame.time.get_ticks() - self.animation_update_time > jump_animation_frame_cooldown:
				self.animation_update_time = pygame.time.get_ticks()
				self.frame_index += 1
			# Check for if the jump animation has reached the end of its animation	
			if self.frame_index >= len(self.animation_frames_list[self.action]):
				# Set the last frame of the Jump animation frames to be the current frame
				self.frame_index = len(self.animation_frames_list[self.action]) - 1

			# If the player lands back onto the ground, set the action to be idle again
			if self.on_ground == True:
				self.idle_animation()

		# Run animation
		if self.action == 2 :
			# Increase the frame index if the cooldown has passed
			if pygame.time.get_ticks() - self.animation_update_time > run_animation_frame_cooldown:
				self.animation_update_time = pygame.time.get_ticks()
				self.frame_index += 1

			# Check for if the idle animation has reached the end of its animation
			if self.frame_index >= len(self.animation_frames_list[self.action]):
				# Reset the animation (i.e. loop it)
				self.frame_index = 0

		#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# Check if we need to flip the player's image

		# When moving left
		if self.flip_image == True:
			# Flip the image (Facing right originally, so make it face left)
			self.image  = pygame.transform.flip(self.image, True, False)
		# When moving right
		if self.flip_image == False:
			# Flip the flipped image, (Facing left now so make it face left)
			self.image = pygame.transform.flip(pygame.transform.flip(self.image, True, False), True, False) 

	def idle_animation(self):
		# Note: This is so that when switching from one animation type to another, it won't print out the error that the frame index is out of range
		# Reset the frame index to start from the beginning of the animation
		self.frame_index = 0
		# Set the action to idle
		self.action = 0	
		# Set the animation update time to now		
		self.animation_update_time = pygame.time.get_ticks()

	def jump_animation(self):
		# Reset the frame index to start from the beginning of the animation
		self.frame_index = 0
		# Set the action to jumping
		self.action = 1
		# Set the animation update time to now
		self.animation_update_time = pygame.time.get_ticks()

	def run_animation(self):
		# Reset the frame index to start from the beginning of the animation
		self.frame_index = 0
		# Set the action to running
		self.action = 2
		# Set the animation update time to now
		self.animation_update_time = pygame.time.get_ticks()

	def jump(self):
		# Reset gravity 
		self.velocity_y = 0
		# First jump (Only if its the first jump do this)
		if self.on_ground == True:

			# Play the jump animation
			self.jump_animation()
			# Jump
			self.velocity_y -= 18
			self.on_ground = False
			self.can_double_jump = True
		# Go for double jump (Only if its during the first jump)
		elif self.can_double_jump == True:

			# Set the player to jump again, resetting the jump animation
			self.jump_animation()

			# Jump again
			self.velocity_y -= 18
			self.can_double_jump = False

	

	def powerup_update(self):

		# Always draw the powerup icons
		screen.blit(peach_status_icon_image,(screen_width - 270, screen_height - 78))
		screen.blit(double_score_status_icon_image,(screen_width - 370, screen_height - 78))
		screen.blit(faster_movement_speed_status_icon_image,(screen_width - 950 , screen_height - 78))

		# Check if the peach powerup was picked up
		if self.peach_status == True:
			# For the duration of the effects	
			if self.peach_amount_of_time > 0: 
				# Constantly update the amount of time left of the peach powerup.
				if (pygame.time.get_ticks() - self.peach_picked_up_time) > 1 :
					# Minus the time that has passed, whilst also adding any time that the player was in the menu.
					self.peach_amount_of_time = (self.peach_amount_of_time + self.in_menu_time) - (pygame.time.get_ticks() - self.peach_picked_up_time)
					self.peach_picked_up_time = pygame.time.get_ticks()
				# Draw the text displaying the amount of time left for the powerup
				draw_text(': ' + str(round(self.peach_amount_of_time / 1000,2))   , score_font, WHITE, screen_width - 230, screen_height - 70)
			# If the effect has worn off, that means that the player is no longer invulnerable anymore
			else:
				self.peach_status = False
				# In the case that the amount of time has become negative, set it back to 0.
				self.peach_amount_of_time = 0
		# Whenever the peach powerup isn't activated
		elif self.peach_status == False:
			draw_text(': 0.00'   , score_font, WHITE, screen_width - 230, screen_height - 70)


		# Check if the double score powerup was picked up
		if self.double_score_status == True: 
			#For the duration of the effect
			if self.double_score_powerup_amount_of_time > 0:
				# Constantly update the amount of time left of the double score powerup
				if (pygame.time.get_ticks() - self.double_score_powerup_picked_up_time) > 1:
					# Minus the time that has passed, whilst also adding any time that the player was in the menu. 
					self.double_score_powerup_amount_of_time = (self.double_score_powerup_amount_of_time + self.in_menu_time) - (pygame.time.get_ticks() - self.double_score_powerup_picked_up_time)
					self.double_score_powerup_picked_up_time = pygame.time.get_ticks()

				# Draw the double score status text
				draw_text(': ' + str(round(self.double_score_powerup_amount_of_time / 1000,2))   , score_font, WHITE, screen_width - 330, screen_height - 70)
			else:
				# Reset the score powerup multiplier to default
				self.double_score_powerup_multiplier = 1
				# Set the status back to False, as the effect has worn off
				self.double_score_status = False 
				# In the case that the amount of time has become negative, set it back to 0.
				self.double_score_powerup_amount_of_time = 0

		# Whenever the double score powerup isn't activated
		elif self.double_score_status == False:
			draw_text(': 0.00'   , score_font, WHITE, screen_width - 330, screen_height - 70)



		# Check if the faster movement speed powerup was picked up 
		if self.faster_movement_speed_status == True:
			 # For the duration of the effect
			 if self.faster_movement_speed_powerup_amount_of_time > 0:
			 	# Constantly update the amount of time left of the faster movement speed powerup
			 	if (pygame.time.get_ticks() - self.faster_movement_speed_powerup_picked_up_time) > 1:
			 		# Minus the time that has passed, whilst also adding any time that the player was in the menu.
			 		self.faster_movement_speed_powerup_amount_of_time = (self.faster_movement_speed_powerup_amount_of_time + self.in_menu_time) - (pygame.time.get_ticks() - self.faster_movement_speed_powerup_picked_up_time)
			 		self.faster_movement_speed_powerup_picked_up_time = pygame.time.get_ticks()

			 	# Draw the faster movement speed status text
			 	draw_text(': ' + str(round(self.faster_movement_speed_powerup_amount_of_time / 1000, 2)), score_font, WHITE, screen_width - 910, screen_height -70)

			 	# Set the speed to 1.5 times the normal speed
			 	self.speed_multiplier = 1.5
			 else:
			 	# Set the status back to false once the effect wears off
			 	self.faster_movement_speed_status = False
			 	# Set the movement speed back to default
			 	self.speed_multiplier = 1
			# Whenever the faster movement speed powerup isn't activated
		elif self.faster_movement_speed_status ==  False:
			draw_text(': 0.00'   , score_font, WHITE, screen_width - 910, screen_height - 70)

	def update(self):
		dx = 0
		dy = 0

		#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# Horizontal movement
		key = pygame.key.get_pressed()
		# Check if the a key is being pressed
		if key[pygame.K_a]:
			# Flip the image (as the original image faces right)
			self.flip_image = True
			# Only while the player is on the ground, change the animation to Run (because if they are in the air I want it to remain as the jump animation)
			# Note: This 2nd check is so that it doesn't constantly set the frame index as 0 whilst running (otherwise the animation would never play)			
			if self.on_ground == True and self.action != 2:		
				self.run_animation()
			dx -= 14 * self.speed_multiplier


		# Check if the d key is being pressed
		if key[pygame.K_d]:
			# Set the image back to default 
			self.flip_image = False
			# Only while the player is on the ground, change the animation to Run (because if they are in the air I want it to remain as the jump animation)
			# Note: This 2nd check is so that it doesn't constantly set the frame index as 0 whilst running (otherwise the animation would never play)
			if self.on_ground == True and self.action != 2:
				self.run_animation()
			dx += 14 * self.speed_multiplier

		# Check if none of these keys are being pressed and if the current action is running
		# Note: This means that when the player stops running, it will go back to the idle animation
		if key[pygame.K_a] == False and key[pygame.K_d] == False and self.action == 2:
			# Switch to the idle animation
			self.idle_animation()

		# Vertical movement
		# Handle gravity 
		self.velocity_y += 1
		if self.velocity_y >= 15:
			# Limit gravity
			self.velocity_y = 15

		dy += self.velocity_y


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
			# The player should be on ground
			self.on_ground = True
			# Note: Not sure what the point of including dy = 0 is
			#dy = 0



		#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def draw(self):
		# Draw player onto screen
		#screen.blit(self.image, (self.rect.x - (23 * self.scale), self.rect.y - (16 * self.scale)))
		screen.blit(self.image, (self.rect.x - 20, self.rect.y))
		#pygame.draw.rect(screen, BLUE, self.rect, 2)
		
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

		# Combo variable
		self.combo_multiplier = 1
		self.score_added = 0

		# Powerups
		self.in_menu_time = 0 # Used to add onto the powerup timers so that when the player pauses the game, the powerup timer stays as it was prior to opening the paused menu

		# Increase staff travel speed
		self.increased_staff_travel_speed_status = False
		self.increased_staff_travel_speed_powerup_picked_up_time = 0
		self.increased_staff_travel_speed_powerup_amount_of_time = 0
		self.travel_speed_divisor = 6 # This is the value used to determine how quick the staff will travel to the clicked mouse position, 6 is the default value

		# Longer staff
		self.longer_staff_status = False

	def powerup_update(self, x, y):
		## Always draw the icon image
		screen.blit(longer_staff_status_icon_image,(screen_width - 520 - 230, screen_height - 78))
		screen.blit(increased_staff_travel_speed_status_icon_image, (screen_width - 850, screen_height - 78))

		# Only if a staff has been placed onto the map can these checks and operations happen (An error would occur if the player picked up the powerup without a staff)
		if staff_count > 0:
			# If the longer staff powerup was picked up then do this:
			# Note: The staff will scale to a certain size and will stay like that until it is picked up. (It is a permanent status for the current instance of the staff)
			if self.longer_staff_status == True:
				# Resize the image of the staff and declare a new rect around the staff
				self.image = pygame.transform.scale(self.image,( (48 * self.scale) * 2, (48 * self.scale * 2) ))
				# Note: self.image_copy is the image that is constantly being blitted onto the screen
				self.image_copy = self.image
				self.rect = self.image_copy.get_rect()
				self.rect.center = (x,y)

				# Draw text for the longer staff status icon
				draw_text(': ', score_font, WHITE, screen_width - 711, screen_height - 70) # x co ord = (screen_width - 480) - 6, this was changed because I wanted the colon to be white
				draw_text('Enabled ', score_font, GREEN, screen_width - 700, screen_height - 70)

			# If the powerup hasn't been activated yet, draw a different set of text
			elif self.longer_staff_status == False: 
				# Draw a different set of text 
				draw_text(':', score_font, WHITE, screen_width - 711, screen_height - 70)
				draw_text('Disabled ', score_font, RED, screen_width - 700, screen_height - 70)

				# Once all of these things have happened, set the status back to False. 
				# Note: There is no point doing this as it is reset when a new instance is made 	

			# If the increased staff travel speed powerup was picked up then:
			if self.increased_staff_travel_speed_status == True:
				if self.increased_staff_travel_speed_powerup_amount_of_time > 0:
					# Constantly update the amount of time left of the increased staff travel speed powerup
					if (pygame.time.get_ticks() - self.increased_staff_travel_speed_powerup_picked_up_time) > 1:
						# Minus the time that has passed, whilst also adding any time that the player was in the menu
						self.increased_staff_travel_speed_powerup_amount_of_time = (self.increased_staff_travel_speed_powerup_amount_of_time + self.in_menu_time) - (pygame.time.get_ticks() - self.increased_staff_travel_speed_powerup_picked_up_time)
						self.increased_staff_travel_speed_powerup_picked_up_time = pygame.time.get_ticks()

					# Set the travel speed divisor to be smaller (making it travel to the mouse position faster)
					self.travel_speed_divisor = 4
					# Draw text for the increased staff travel speed powerup
					draw_text(': ' + str(round(self.increased_staff_travel_speed_powerup_amount_of_time / 1000,2))   , score_font, WHITE, screen_width - 810, screen_height - 70)
				# If the effect has run out
				else:
					# Set travel_speed_divisor back to its default value
					self.travel_speed_divisor = 6
					# Set the status back to default
					self.increased_staff_travel_speed_status = False
			# While the powerup isn't picked up, draw this text next to the icon
			elif self.increased_staff_travel_speed_status == False:
				draw_text(': 0.00', score_font, WHITE, screen_width - 810, screen_height - 70)



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
			# Reset combo back to default
			self.combo_multiplier = 1

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

#staff = Wukong_Staff(screen_width // 2, screen_height // 2

background = Background(0,0, screen)
ground = Ground(0, screen_height - 130, screen)

menu = MainMenu(0,0, screen)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Groups
player_group = pygame.sprite.Group()
player_group.add(player)

staff_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
circle_effect_group = pygame.sprite.Group()
text_effect_group = pygame.sprite.Group()
peach_powerup_group = pygame.sprite.Group()
double_score_powerup_group = pygame.sprite.Group()
longer_staff_powerup_group = pygame.sprite.Group()
faster_movement_speed_powerup_group = pygame.sprite.Group()
increased_staff_travel_speed_powerup_group = pygame.sprite.Group()

# A group that holds all of the groups I want to be seen once the 20 seconds are over
all_groups = []
all_groups.append(staff_group)
all_groups.append(enemy_group)
all_groups.append(peach_powerup_group)
all_groups.append(double_score_powerup_group)
all_groups.append(longer_staff_powerup_group)
all_groups.append(faster_movement_speed_powerup_group)
all_groups.append(increased_staff_travel_speed_powerup_group)


# Variables (MOVE UP LATER)

spawn_powerups_in_menu_time = [0,0] # First element is for collectible powerups, 2nd element is for peaches


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# GAME LOOP

run = True
while run:
	
	# Limit FPS to 60
	clock.tick(60)	

	# If the mute music variable is True (More detail inside the Button program)
	if menu.mute_music == True:
		# Then mute the music
		pygame.mixer.music.set_volume(0)
	# Else, if the mute music variable is False
	elif menu.mute_music == False:
		# Then unmute the music
		pygame.mixer.music.set_volume(0.025)
		


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# STARTING MENUS

	# Only update the menus when we are still looking at menus (otherwise it will bug out ingame when clicking over where the buttons positions should be)
	# Note: must keep menu.show_controls_menu, otherwise the menu class won't be updated while we are in the controls menu
	if menu.show_main_menu == True or menu.show_controls_menu == True:
		# Update menus to show the main menu
		menu.update()
		# In the main menu, draw the high score (This is so that it doesn't also get drawn in the controls menu)
		if menu.show_main_menu == True:
			# Draw the high score achieved by the player
			#draw_text('High score: ' + str(high_score), score_font, WHITE, 425, 315)

			draw_text('High score: ' , score_font, WHITE, 425, 315)
			draw_text(str(high_score), score_font, GOLD, 530, 315)

	# If neither the main or controls menun is being shown, that means the user clicked the 'Play' button, so start the game.
	if menu.show_main_menu == False and menu.show_controls_menu == False:

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# Only play the game during the 20 second countdown
		if amount_of_time > 0 and menu.show_paused_menu == False:	

			# Note: The allow clicking attibrute is responsible for allowing the player to click once the play button is clicked (as it is originally set to False)
			if menu.allow_clicking == True:
				allowed_to_click = True 
				menu.allow_clicking = False	

			#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	

			# Constantly update the countdown time
			if pygame.time.get_ticks() - menu.play_button_clicked_time > 1 and menu.show_paused_menu == False:
				# Add the amount of time the player was in the menu to the amount of time left (that way they don't lose time whilst inside the menus), and then minus how much time has passed since the last second was taken away
				amount_of_time = (amount_of_time  + menu.in_menu_time) -  (pygame.time.get_ticks() - menu.play_button_clicked_time) 
				# Reset the time so that it carries on counting per second
				menu.play_button_clicked_time = pygame.time.get_ticks()

				# Copy the "in menu time" to the attributes of the player (and staff if there is one)
				# Note: This is because we also need the time to update the powerup times as well (because we would have reset menu.in_menu_time by the time we use player.powerup_update())
				player.in_menu_time = menu.in_menu_time
				
				# Set the first and second value of the list to the time inside the menu, only if the list value for the first element was already empty and the in menu time is not zero.
				# Note: There is room for optimisation here (Maybe instead of using so many different menu times, just use a single one that is global)
				if spawn_powerups_in_menu_time[0] == 0 and menu.in_menu_time > 0:
					spawn_powerups_in_menu_time[0] = menu.in_menu_time
					spawn_powerups_in_menu_time[1] = spawn_powerups_in_menu_time[0]

				if staff_count > 0:
					staff.in_menu_time = menu.in_menu_time


				# Reset the in menu time
				menu.in_menu_time = 0

				# Reset the list so that new entered menu and left menu times can be recorded
				menu.menu_time_list = []	


			#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			# Increasing difficulty as time passes

			# If 4 seconds have passed
			if amount_of_time <= 16000:
				# Increase spawn rate of arrows
				enemy_spawning_cooldown = 400 # Original = 500
			# If 8 seconds have passed
			if amount_of_time <= 12000:	
				# Increase the speed of all arrows
				for enemy in enemy_group:
					enemy.speed_multiplier = 1.1
			# If 12 seconds have passed
			if amount_of_time <= 8000:
				# Increase spawn rate of arrows
				enemy_speed_cooldown = 300
			# If 16 seconds have passed
			if amount_of_time <= 4000:
				# Increase the speed of all arrows
				for enemy in enemy_group:
					enemy.speed_multiplier = 1.2

			#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			#cursor_position = pygame.mouse.get_pos() # Note: Moved this to the top of the code to avoid errors 
			#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			# WORLD TILES

			# Draw the background and the floor (They are both animated so I made individual classes for both of them)
			background.draw()
			background.update_animation()
			ground.draw()

 
			# Draw every tile inside of the tile list
			for tile in tile_list:
				# Check if the width isn't 300 (then it is one of the smaller tiles)			
				if tile.width != 300:
					# If it is one of the tiles on the right
					if tile.x == 700:
						# Then flip the tile in the x-axis and draw it onto the screen
						screen.blit(pygame.transform.flip(small_world_tile, True, False), (tile.x, tile.y))
					else:
						# Otherwise, draw the tile normally.
						screen.blit(small_world_tile, (tile.x, tile.y))
				# If the width is 300, this means that it is the medium tile (the one in the middle)
				else:
					screen.blit(medium_world_tile,(tile.x, tile.y))


			# Draw the translucent countdown timer
			draw_alpha_text(str(round(amount_of_time / 1000 , 1)), countdown_font, countdown_colour, (screen_width / 2) - 100, (screen_height / 2) - 450)

			# Draw score text
			draw_text('Score: ' + str(total_score), score_font, WHITE, screen_width - 150, screen_height - 70)

			#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			# Update and draw the player
			player.draw()
			player.update()
			player.update_animation()


			# ENEMIES

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
							# Play sound effect
							enemy_destroyed_sound.play()
							# Circle effects
							# If there is a collision instantiate a circle effect at where the enemy died
							circle = CircleEffect(staff.rect.centerx, staff.rect.centery, 0, 5) # (x, y, radius, line thickness)
							# Note: originally we drew the circle effect at the (enemy.rect.centerx, enemy.rect.centery), drawing it at the staff makes more sense and fixes the "bug"
							circle_effect_group.add(circle)


							# Score
							# Keep track of the score to be added (multiplied by the current combo multiplier, which is reset back to 1 every time the staff hits the ground
							staff.score_added = score_add * staff.combo_multiplier

							# Increment combo
							# Note: Multiply it by double score multiplier, which is only activated when the double score powerup is picked up

							total_score += staff.score_added * player.double_score_powerup_multiplier 
							# Draw the score added onto the screen
							combo_text = TextEffect(staff.rect.centerx, staff.rect.centery,'+' + str(staff.score_added * player.double_score_powerup_multiplier), WHITE)
							text_effect_group.add(combo_text)

							# Multiply the combo multiplier by 2 
							# Note: Increase the combo multiplier here because then when the next enemy is hit, the score added will already be 2x as much
							staff.combo_multiplier *= 2



				# First check for rect collision between the player and enemies
				if pygame.sprite.spritecollide(player, enemy_group, False):
					# Look for a more accurate collision between the player and enemies
					if pygame.sprite.spritecollide(player, enemy_group, True, pygame.sprite.collide_mask):
						# Check if the peach status is enabled, if it is then the player will not lose score
						if player.peach_status == True:
							# Draw the peach immunity text effect instead, indicating that the player is immune to losing score
							peach_immunity_text = TextEffect(player.rect.centerx, player.rect.centery,'-' + str(0), GOLD)
							text_effect_group.add(peach_immunity_text)

						# If it is disabled, the player can lose score
						else:
							# Subtract score from the total score
							total_score -= score_subtract
							# NOTE ADD MORE HERE E.G SOUND EFFECTS, COINS BEING REMOVED, ETC.
							score_subtract_text = TextEffect(player.rect.centerx, player.rect.centery,'-' + str(score_subtract), RED)
							text_effect_group.add(score_subtract_text)


			# Update enemies
			enemy_group.update()
			# Update circle effects
			circle_effect_group.update()


			#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			# Powerups
				

			# Spawn peach powerup
			# Note: Every 8 seconds, a peach powerup is spawned 

			# Check if enough time has passed since the start of the game
			if ((pygame.time.get_ticks() - spawn_powerups_in_menu_time[1]) - game_started_time_peach) > peach_spawning_cooldown:
				#print(pygame.time.get_ticks() - game_started_time_peach)
				# Re-use random_x variable from the enemy randomized spawns
				if len(peach_powerup_group) == 0: # Only spawn a peach powerup when there are none in the world already
					peach = Peach_P(random_x, - 64) # I want the peaches to spawn off screen at first and fall down
					peach_powerup_group.add(peach)
					# Set the time of the last peach spawned to the current time
					game_started_time_peach = pygame.time.get_ticks()

					spawn_powerups_in_menu_time[1] = 0



			# Spawn collectible powerups
			#Note: #possible_spawning_locations = [ [(200 + 75) - (41.25 // 2) , 750 - 40], [(200 + 75) - (41.25 // 2) , 250 - 40], [350 + 150 - (41.25 // 2), 500 - 40], [(700 + 75) - (41.25 // 2), 250 - 40], [(700 + 75) - (41.25 // 2), 750 - 40]] 
			# print(pygame.time.get_ticks() - game_started_time_collectible_powerups)

			# If the time between the game started and now has been the length of the collectible powerups cooldown, then start spawning powerups
			# Note: added the spawn_powerups_in_menu_time[0] to minus any time that was spent inside of the menus
			if ((pygame.time.get_ticks() - spawn_powerups_in_menu_time[0]) - game_started_time_collectible_powerups)  > collectible_powerups_spawning_cooldown:
				# Choose a random spawning location
				# Limit the number of collectible powerups to 2 
				if num_of_collectible_powerups <= 2:

					# Pick a random index from the list of indexes
					random_index = random.randint(0,len(random_index_list) - 1) #random_index_list[0] or [1] or [2] or [3] or [4]

					# Pick between four numbers, which will decide which powerup is chosen.
					choose_powerup_number = random.randint(1,4)

					if choose_powerup_number == 1:
						# Instantiate a powerup at one of these locations
						double_score_powerup = DoubleScore_P(possible_spawning_locations[random_index_list[random_index]][0], possible_spawning_locations[random_index_list[random_index]][1])
						double_score_powerup_group.add(double_score_powerup)
						# Increment the number of collectible powerups spawned
						num_of_collectible_powerups += 1
					elif choose_powerup_number == 2:
						# Instantiate a powerup at one of these locations
						longer_staff_powerup = LongerStaff_P(possible_spawning_locations[random_index_list[random_index]][0], possible_spawning_locations[random_index_list[random_index]][1])
						longer_staff_powerup_group.add(longer_staff_powerup)	
						# Increment the number of collectible powerups spawned
						num_of_collectible_powerups += 1
					elif choose_powerup_number == 3:
						# Instantiate a powerup at one of these locations
						faster_movement_speed_powerup =  FasterMovementSpeed_P(possible_spawning_locations[random_index_list[random_index]][0], possible_spawning_locations[random_index_list[random_index]][1])
						faster_movement_speed_powerup_group.add(faster_movement_speed_powerup)	
						# Increment the number of collectible powerups spawned
						num_of_collectible_powerups += 1
					elif choose_powerup_number == 4:
						# Instantiate a powerup at one of these locations
						increased_staff_travel_speed_powerup =  IncreasedStaffTravelSpeed_P(possible_spawning_locations[random_index_list[random_index]][0], possible_spawning_locations[random_index_list[random_index]][1])
						increased_staff_travel_speed_powerup_group.add(increased_staff_travel_speed_powerup)	
						# Increment the number of collectible powerups spawned
						num_of_collectible_powerups += 1


					#print("spawned at", pygame.time.get_ticks() - spawn_powerups_in_menu_time[0])
					#  Pop the index from the random index list, so it cannot be picked again
					random_index_list.pop(random_index)

					# Reset the spawn_powerups_in_menu_time[0]
					spawn_powerups_in_menu_time[0] = 0

					# Set the last time a collectible powerup was spawned to be now
					game_started_time_collectible_powerups = pygame.time.get_ticks()

					# Check if the random index list has anymore indexes left, if it doesn't this means all locations have been used already, in that case, declare the random_index list again
					# Note: I made an index list because remove locations from possible_spawning_locations would just shift everything down.
					if len(random_index_list) == 0:
						random_index_list = [0,1,2,3,4]


			#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			# Collision

			# Collision with peaches
			if pygame.sprite.spritecollide(player, peach_powerup_group, False):
				if pygame.sprite.spritecollide(player, peach_powerup_group, True, pygame.sprite.collide_mask):
					# Play sound effect
					powerup_sound.play()

					# Add score to the total score
					total_score += (score_add * 10) * player.double_score_powerup_multiplier # Adds 100 to 200 score to the player's total score (depends on whether the x2 powerup is enabled)
					# Draw the text that displays how much was added to the score
					peach_text = TextEffect(player.rect.centerx, player.rect.centery,'+' + str((score_add * 10) * player.double_score_powerup_multiplier), GOLD)
					text_effect_group.add(peach_text)

					# Record the time when the peach was picked up
					player.peach_picked_up_time = pygame.time.get_ticks()
					# Change peach status variable to True so the status text can be drawn at the bottom
					player.peach_status = True

					# Increase the player peach time
					player.peach_amount_of_time += 8000


			# Collision with collectible powerups
			# Double score powerups
			if pygame.sprite.spritecollide(player, double_score_powerup_group, False):
				if pygame.sprite.spritecollide(player, double_score_powerup_group, True, pygame.sprite.collide_mask):
					# Play sound effect
					powerup_sound.play()
					# Set the powerup effect to True
					player.double_score_status = True
					player.double_score_powerup_multiplier = 2
					# Record the time that the powerup was picked up
					player.double_score_powerup_picked_up_time = pygame.time.get_ticks()
					# Increase the player double score powerup time
					player.double_score_powerup_amount_of_time += 10000
					# Lower then number of collectibles in the map currently 
					num_of_collectible_powerups -= 1

					# Reset the game_started_time_collectible_powerups to be the same as the current time so that it will count 4 seconds from when the player picked up the powerup
					game_started_time_collectible_powerups = pygame.time.get_ticks()


			# Longer staff powerups
			if pygame.sprite.spritecollide(player, longer_staff_powerup_group, False):
				if pygame.sprite.spritecollide(player, longer_staff_powerup_group, True, pygame.sprite.collide_mask):
					# Lower then number of collectibles in the map currently
					num_of_collectible_powerups -= 1
					if staff_count > 0:
						# Play sound effect (Play it only if the staff has been placed out)
						powerup_sound.play()
						# I want to permanently modify the length of the staff for this instance of the staff
						staff.longer_staff_status = True


			# Faster movement speed powerup
			if pygame.sprite.spritecollide(player, faster_movement_speed_powerup_group, False):
				if pygame.sprite.spritecollide(player, faster_movement_speed_powerup_group, True, pygame.sprite.collide_mask):
					# Play sound effect
					powerup_sound.play()					
					# Lower then number of collectibles in the map currently
					num_of_collectible_powerups -= 1
					# Set the powerup effect to True
					player.faster_movement_speed_status = True
					# Get the time that the player picked up the powerup
					player.faster_movement_speed_powerup_picked_up_time = pygame.time.get_ticks()
					# Increase the player double score powerup time
					player.faster_movement_speed_powerup_amount_of_time += 10000


			# Increased staff travel speed powerups
			if pygame.sprite.spritecollide(player, increased_staff_travel_speed_powerup_group, False):
				if pygame.sprite.spritecollide(player, increased_staff_travel_speed_powerup_group, True, pygame.sprite.collide_mask):
					# Lower then number of collectibles in the map currently
					num_of_collectible_powerups -= 1
					if staff_count > 0:
						# Play sound effect
						powerup_sound.play()
						# Record the time this powerup was picked up
						staff.increased_staff_travel_speed_powerup_picked_up_time = pygame.time.get_ticks()
						# Increase the staff powerup time
						staff.increased_staff_travel_speed_powerup_amount_of_time += 10000
						# Set the powerup status to True
						staff.increased_staff_travel_speed_status = True



			# Staff powerups text and icons updating
			# Note: I'm placing this here because these won't be drawn until there is a staff out. Also there is a bug where if you pick up the ITS powerup and then pick up your staff, you will permanently have the speed bonus


			#print(pygame.time.get_ticks() - gbame_started_time_double_score)

			# Update all text effects 
			text_effect_group.draw(screen)
			text_effect_group.update()

			# Update the powerup groups
			# Note: These functions will also draw them onto the screen, these updates are down at the bottom because I want them to be drawn over the staff
			peach_powerup_group.update()
			double_score_powerup_group.update()
			longer_staff_powerup_group.update()	
			faster_movement_speed_powerup_group.update()
			increased_staff_travel_speed_powerup_group.update()

			# Check for if any powerups have been picked up and activate their effects
		
			player.powerup_update()

			# Check for if any powerups have been picked up and activate their effects
			if staff_count > 0:

				# Call the staff powerup update function and feed into the function the current position of the staff
				# Also feed and return the variable travel_speed_divisor into the function
				# Note: This is because the staff will be scaled from that point
				staff.powerup_update(staff.rect.centerx, staff.rect.centery)


			#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			# Mouse position finding
			#mouse_click_position = pygame.mouse.get_pos()

			# If the mouse button has been clicked
			if clicked == True:

				# Don't allow the player to click for a new position
				allowed_to_click = False
				mouse_click_position = pygame.mouse.get_pos()
				# Play staff sound effect
				staff_sound.play()
				#screen.blit(green_reticle_image, cursor_position)
				#print(mouse_click_position)	

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
					movement_y = float(delta_y / staff.travel_speed_divisor)  # Original = 6, With the increased staff travel powerup, it is 2
					if staff.rect.centery > mouse_click_position[1]: # Staff is below the clicked position
						# Increment the staff's y position up
						staff.rect.centery -= movement_y 

					# X - position pathfinding
					movement_x = float(delta_x / staff.travel_speed_divisor)
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

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# PAUSED MENU	
		# If the ESC button has been pressed and the game hasn't finished
		if menu.show_paused_menu == True and amount_of_time > 0 :
			# Let the player see the mouse again
			pygame.mouse.set_visible(True)
			
			# Start updating the menus again
			menu.update()

			# Keep drawing the translucent countdown timer
			draw_alpha_text(str(round(amount_of_time / 1000 , 0)), countdown_font, countdown_colour, (screen_width / 2) - 100, (screen_height / 2) - 450)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# REPLAY MENU
		# If the 20 second countdown has ended then do this:
		elif amount_of_time <= 0 :

			# Check if a new high score was achieved, if it was then set high score as the current score achieved
			if total_score > high_score:
				high_score = total_score
				# Write the score into a new file as a string
				with open('score.txt','w') as file:
					file.write(str(high_score))
		


			# Draw all the items, but do not update them (This will make it seem as if everything has frozen in place)
			background.draw()
			ground.draw()

			# Draw every tile inside of the tile list
			for tile in tile_list:
				# Check if the width isn't 300 (then it is one of the smaller tiles)			
				if tile.width != 300:
					# If it is one of the tiles on the right
					if tile.x == 700:
						# Then flip the tile in the x-axis and draw it onto the screen
						screen.blit(pygame.transform.flip(small_world_tile, True, False), (tile.x, tile.y))
					else:
						# Otherwise, draw the tile normally.
						screen.blit(small_world_tile, (tile.x, tile.y))
				# If the width is 300, this means that it is the medium tile (the one in the middle)
				else:
					screen.blit(medium_world_tile,(tile.x, tile.y))

			player.draw()	

			# Draw all of the groups onto the screen
			for group in all_groups:
				group.draw(screen)

			# Allow the cursor to be seen again
			pygame.mouse.set_visible(True)	

			# Draw slightly faded background (Keep this on top of all of the ingame stuff, menu buttons will be drawn after this)
			screen.blit(faded_surface, (0,0))

			# RESTART MENU 

			# Set the show replay menu variable to true
			menu.show_replay_menu = True 
			# Start updating the menus again
			menu.update()

			# Draw the current score and the highest score achieved
			draw_text('High score: ' , score_font, WHITE, 425, 335)
			draw_text(str(high_score), score_font, GOLD, 530, 335)
			draw_text('Current score: ', score_font, WHITE, 425, 365)
			draw_text(str(total_score), score_font, GOLD, 560, 365)

			# If the replay button was clicked:
			if menu.reset_level == True:
				# Empty all of the groups
				for group in all_groups:
					group.empty()

				if len(circle_effect_group) > 0:
					circle_effect_group.empty()
				if len(text_effect_group) > 0:
					text_effect_group.empty()

				# Return all the variables with the reset_level function
				staff_count,player, allowed_to_click, amount_of_time, total_score, game_started_time_peach, game_started_time_collectible_powerups, num_of_collectible_powerups, random_index_list, starting_enemy_spawned = reset_level(staff_count, player, allowed_to_click, amount_of_time, total_score, game_started_time_peach, game_started_time_collectible_powerups, num_of_collectible_powerups, random_index_list, starting_enemy_spawned)
				menu.reset_level = False



	#-----------------------------------------
	for event in pygame.event.get():
		# If the "x" button on window is clicked, quit the game
		if event.type == QUIT:
			run = False
			pygame.quit()
			sys.exit()
		# Check for when a keyboard button is pressed
		if event.type == pygame.KEYDOWN:

			if event.key == K_SPACE: 
				# Handle jumping
				if player.on_ground == True:
					player.jump()
				elif player.can_double_jump == True:
					player.jump()

			if event.key == K_ESCAPE:
				# If in the main menu and the escape key is pressed, quit the game
				if menu.show_main_menu == True:
					run = False
					pygame.quit()
					sys.exit()
				# If not in the main menu or replay menu (ingame)
				elif menu.show_main_menu == False and menu.show_replay_menu == False:
					# If not in the main menu, then we are ingame and it is pressed 
					menu.show_paused_menu = True
					

		if event.type == pygame.MOUSEBUTTONDOWN and allowed_to_click == True:

			# Set the clicked variable to true - This allows for the mouse position to be found
			clicked = True



	pygame.display.update()
