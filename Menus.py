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
# All buttons are 400 x 125 pixels 

# Main menu display
start_image = pygame.image.load('graphics/Buttons/play_button.png').convert()
quit_image = pygame.image.load('graphics/Buttons/quit_button.png').convert()
title_image = pygame.image.load('graphics/Buttons/title_image.png').convert_alpha()
controls_image = pygame.image.load('graphics/Buttons/controls_button.png').convert()
mute_music_image = pygame.image.load('graphics/Buttons/mute_music_button.png').convert()


# Controls menu display
controls_display_image = pygame.image.load('graphics/Buttons/controls_display.png').convert_alpha() # 750 x 450 pixels
back_image = pygame.image.load('graphics/Buttons/back_button.png').convert() 
powerups_display_image = pygame.image.load('graphics/Buttons/powerups_display.png').convert_alpha()

# Paused menu display
continue_image = pygame.image.load('graphics/Buttons/continue_button.png').convert()

# Replay menu display
replay_image = pygame.image.load('graphics/Buttons/return_to_main_menu_button.png').convert()
game_over_display_image = pygame.image.load('graphics/Buttons/game_over_display.png').convert()

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
		# Note: This were used to fix the bug where if you clicked a the back/replay button(which was over the quit/ controls button originally, it would exit the game because it kept registering it as a click. 
	
		self.button_clicked = pygame.time.get_ticks()	# Used to record when a button (except play button), was clicked

		# Menu times 
		self.menu_time_list = [] # Used to store the time that the user entered and left the paused menu
		self.entered_menu_time = 0 # Tracks when the user entered the paused menu
		self.left_menu_time = 0 # Tracks when the user left the paused menu
		self.in_menu_time = 0 # Holds the difference in time between when the player entered and left the paused menu

		# Replay button
		self.reset_level = False

		# If the player has pressed the play button, allow clicking to happen again
		# Note: This was used in part when fixing the clicking system with the menus and ingame in general
		self.allow_clicking = False

		# Music
		self.mute_music = False


	def update(self): 

		# Keep drawing the background regardless of what menu it is 
		# Note: This also helps with the issue of clearing the old controls text
		if self.show_main_menu or self.show_controls_menu or self.show_paused_menu:
			background.draw()
			background.update_animation()
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

				# Allow the player to click
				self.allow_clicking = True



			# Draw and check if the controls button was clicked				

			# Note: the button clicked condition is used to fix the bug where if you click e.g. return to main menu in replay menu, since it was over the controls / quit button, it would be registered as a click 
			if controls_button.draw() and (pygame.time.get_ticks() - self.button_clicked > 100):
				# Set the variable to start showing the controls menu to True 
				self.show_controls_menu = True

			# Draw and check if the quit button was clicked
			if quit_button.draw() and pygame.time.get_ticks() - self.button_clicked > 100:
					# Set run as false and quit the program
					run = False
					pygame.quit()
					# Note: sys.exit is added to get rid of "pygame.error: video system not initialized"
					sys.exit()

			# Draw and check if the music button was clicked
			if mute_music_button.draw() and pygame.time.get_ticks() - self.button_clicked > 100:
				# If the music is on and the player wants to mute the music
				if self.mute_music == False:
					# Set the mute music variable to True
					self.mute_music = True
					#print("mute_music")
				elif self.mute_music == True:
					self.mute_music = False
					#print("unmute music")

		# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# CONTROLS MENU

		if self.show_controls_menu == True:
			# Don't show the main menu (They cannot be drawn at the same time)
			self.show_main_menu = False
			# Don't show the paused menu (They cannot be drawn at the same time)
			self.show_paused_menu = False


			# Show the controls menu
			screen.blit(powerups_display_image, (0, -60))
			screen.blit(controls_display_image, (-50, 433))


			# Draw the back button and check if its been clicked
			if back_button.draw() == True:
				self.button_clicked = pygame.time.get_ticks()
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
			# Get the time that the player entered the menu:
			# Note: This is because I want to track the time that the player is in the menu and add that onto the amount of time so that it doesn't continue counting down even when the 
			# Note PT2: player is in the menu.


			if len(self.menu_time_list) < 1:
				self.entered_menu_time = pygame.time.get_ticks()
				#print("entered", self.entered_menu_time)			
				self.menu_time_list.append(self.entered_menu_time)


			# Draw the paused menu

			# Draw and check for if the controls button is clicked
			if continue_button.draw():
				# Don't show the paused menu anymore
				self.show_paused_menu = False
				# Find when the player left the menu
				self.left_menu_time = pygame.time.get_ticks()
				self.menu_time_list.append(self.left_menu_time)
				#print("left",self.left_menu_time)


				self.in_menu_time = self.menu_time_list[1] - self.menu_time_list[0]



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


			# Draw and check if the music button was clicked
			if mute_music_button.draw() and pygame.time.get_ticks() - self.button_clicked > 100:
				# If the music is on and the player wants to mute the music
				if self.mute_music == False:
					# Set the mute music variable to True
					self.mute_music = True
					#print("mute_music")
				elif self.mute_music == True:
					self.mute_music = False
					#print("unmute music")


		# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# REPLAY MENU

		if self.show_replay_menu == True:
			# Draw replay menu
			# This image is 600 x 188 pixels
			self.surface.blit(game_over_display_image, (200, 100)) 
			# Draw and check for if the replay button is clicked
			if replay_button.draw():
				# Show the main menu instead of the replay menu
				self.show_replay_menu = False
				# Reset the level
				self.reset_level = True
				# Start showing the main menu
				self.show_main_menu = True
				# Set the last menu visited to be the main menu (This is because we don't want the player being able to go back to the replay menu)
				self.last_menu_visited = 0
				# Register the return to main menu button as being clicked
				self.button_clicked = pygame.time.get_ticks()

			# Draw and check for if the quit button is clicked
			if quit_button_2.draw():
				# Set run as false and quit the program
				run = False
				pygame.quit()
				# Note: sys.exit is added to get rid of "pygame.error: video system not initialized"
				sys.exit()		



		


# Buttons
# Note: 300 = (screen_width / 2) - 200 [200 is half the size of the button image]

# Main menu
start_button = Button(300, 375, start_image)
controls_button = Button(300, 535, controls_image)
quit_button = Button(300, 695, quit_image)
mute_music_button = Button(850, 850, mute_music_image)

# Controls menu 
back_button = Button(300, 840, back_image)


# Paused menu 
continue_button = Button(300, 375, continue_image)

# Replay menu 
# Replay image is 400 x 125 pixels wide
# 428 = 378 + 50, 588 = 538 + 50
replay_button = Button(300, 428, replay_image)
quit_button_2 = Button(300, 588, quit_image)

# Background instance to draw backgrounds even in the menus
background = Background(0,0, screen)


