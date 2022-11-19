import pygame, sys
from Background import Background


# Initialise fonts
# Note: You can also do pygame.init(), but I think that would be "longer" to initialise
pygame.init()
#pygame.font.init()

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

# Buttons 

# Main menu display
start_image = pygame.image.load('graphics/Buttons/MainMenu/play_button.png').convert()
quit_image = pygame.image.load('graphics/Buttons/MainMenu/quit_button.png').convert()
title_image = pygame.image.load('graphics/Buttons/MainMenu/title_image.png').convert_alpha()
controls_image = pygame.image.load('graphics/Buttons/MainMenu/controls_and_info_button.png').convert()


# Controls menu display
controls_display_image = pygame.image.load('graphics/Buttons/ControlsMenu/controls_display.png').convert_alpha() # 750 x 450 pixels
back_image = pygame.image.load('graphics/Buttons/ControlsMenu/back_button.png').convert() 
powerups_display_image = pygame.image.load('graphics/Buttons/ControlsMenu/powerups_display.png').convert_alpha()

# Paused menu display
continue_image = pygame.image.load('graphics/Buttons/PausedMenu/continue_button.png').convert()

# Replay menu display
replay_image = pygame.image.load('graphics/Buttons/ReplayMenu/replay_button.png').convert()

# Font
creator_text_font = pygame.font.SysFont('Bahnschrift', 20)

def draw_text(text, font, text_colour, x, y):
	image = font.render(text, True, text_colour)
	screen.blit(image, (x,y))



class Button(pygame.sprite.Sprite):
	def __init__(self, x, y, image):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False


	def draw(self):
		clicked_button = False

		# Get the mouse position of the user
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			# If the player clicks their left mouse button 
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				clicked_button = True

			# If the player has let go of the left mouse button
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False

		# Draw the button
		screen.blit(self.image, self.rect)
		return clicked_button

class MainMenu():
	def __init__(self, x, y, surface):
		# Surface that the menu will be drawn onto
		self.surface = surface
		# Button list
		self.button_list = []

		# Game states
		self.show_main_menu = True # Variable to hold whether we show the main menu or nots
		self.show_controls_menu = False # Variable to hold whether we show the controls menu or not
		self.show_paused_menu = False # Variable to hold whether we show the paused menu or not
		self.show_replay_menu = False # Variable to hold whether we show the replay menu or not

		self.last_menu_visited = 0 # 0 = Main menu, 1 = Paused menu , 2 = Replay menu holds the menu where the controls button was clicked from 


		# Button clicked times

		self.play_button_clicked_time = pygame.time.get_ticks() # Used to record when the play button was clicked

		# Note: This was used to fix the bug where if you clicked a the back button(which was over the quit button originally, it would exit the game because it kept registering it as a click. 
		self.back_button_clicked = pygame.time.get_ticks()	# Used to record when the back button was clicked. 
		

		# Replay button
		self.reset_level = False

	def update(self): 

		# Keep drawing the background regardless of what menu it is 
		# Note: This also helps with the issue of clearing the old controls text
		background.draw()
		# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# MAIN MENU
		if self.show_main_menu == True:

			# Draw the buttons
			# Note: There is probably a way to optimise this code, maybe a dictionary (Talking about the stuff above this)

			# Draw the title image onto the screen
			self.surface.blit(title_image, (150,100))

			# Draw text displaying that I created it
			draw_text("Created by: LyleW473", creator_text_font, WHITE, 400, 253)

			# Draw and check if the start button was clicked
			if start_button.draw() == True: # If the variable returned from calling the draw function, clicked_button, is true then:
				# Set the show main menu variable to false
				self.show_main_menu = False
				# Set the time that the play button was clicked to now
				self.play_button_clicked_time = pygame.time.get_ticks()

			# Draw and check if the controls button was clicked				
			if controls_button.draw():
				# Set the variable to start showing the controls menu to True 
				self.show_controls_menu = True

			# Draw and check if the quit button was clicked
			if quit_button.draw() and (pygame.time.get_ticks() - self.back_button_clicked > 100):
				# Set run as false and quit the program
				run = False
				pygame.quit()
				# Note: sys.exit is added to get rid of "pygame.error: video system not initialized"
				sys.exit()
		# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# CONTROLS MENU

		if self.show_controls_menu == True:
			# Don't show the main menu (They cannot be drawn at the same time)
			self.show_main_menu = False
			# Don't show the paused menu (They cannot be drawn at the same time)
			self.show_paused_menu = False


			# Show the controls menu
			screen.blit(powerups_display_image, (0, -25))
			screen.blit(controls_display_image, (-50, 450))


			#draw_text("A - Move left", controls_text_font, WHITE, 700, 400)
			#draw_text("D - Move right", controls_text_font, WHITE, 700, 440)
			#draw_text("Spacebar - Jump", controls_text_font, WHITE, 700, 480)


			# Draw the back button and check if its been clicked
			if back_button.draw() == True:
				self.back_button_clicked = pygame.time.get_ticks()
				# Don't show the controls menu
				self.show_controls_menu = False

				# Check in which menu, the controls button was clicked (0 = main menu, 1 = paused menu)
				if self.last_menu_visited == 0:
					# Show the main menu again
					self.show_main_menu = True
				elif self.last_menu_visited == 1:
					# Show the paused menu again
					self.show_paused_menu = True

	
		# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# PAUSED MENU

		if self.show_paused_menu == True:
			# Draw the paused menu

			# Draw and check for if the controls button is clicked
			if continue_button.draw():
				# Don't show the paused menu anymore
				self.show_paused_menu = False




			# Draw and check for if the controls button is clicked
			if controls_button.draw(): 
				self.show_controls_menu = True
				# Don't show the paused menu anymore
				self.show_paused_menu = False
				# Set the last menu visited to be the paused menu
				self.last_menu_visited = 1

			# Draw and check for if the quit button is clicked
			if quit_button.draw():
				# Set run as false and quit the program
				run = False
				pygame.quit()
				# Note: sys.exit is added to get rid of "pygame.error: video system not initialized"
				sys.exit()		

		# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

		if self.show_replay_menu == True:
			# Draw replay menu
			if replay_button.draw():
				print("replay")
				# Show the main menu instead of the replay menu
				self.show_replay_menu = False
				# Set the time that the play button was clicked to now
				self.play_button_clicked_time = pygame.time.get_ticks()
				# Set the reset level variable to be True, this will allow for the reset_level() function inside main.py to be called.
				self.reset_level = True




			# Draw and check for if the quit button is clicked
			if quit_button.draw():
				# Set run as false and quit the program
				run = False
				pygame.quit()
				# Note: sys.exit is added to get rid of "pygame.error: video system not initialized"
				sys.exit()		


		


# Buttons
# Note: 340 = (screen_width / 2) - 160 [160 is half the size of the button image]
# Main menu
start_button = Button(340, 375, start_image)
controls_button = Button(340, 525, controls_image)
quit_button = Button(340, 675, quit_image)

# Controls menu 
back_button = Button(340, 850, back_image)

# Paused menu 
continue_button = Button(340, 375, continue_image)

# Replay menu 
replay_button = Button(340, 525, replay_image)

# Background instance to draw backgrounds even in the menus
background = Background(0,0, screen)


