#!/usr/bin/env/python3
import math
import pygame
import sys
import engine

PIN_LOCATIONS = [
[720,30],		#pin 1
[730.4,24],		#pin 2
[730.4,36],		#pin 3
[740.8,18],		#pin 4
[740.8,30],		#pin 5
[740.8,42],		#pin 6
[751.2,12],		#pin 7
[751.2,24], 	#pin 8
[751.2,36],		#pin 9
[751.2,48] 		#pin 10
]

def main():
	print("Not for human consumption. Please evacuate the premises.")

if name == '__main__':
	main()

class BowlingGame: #@todo(bumsik): add a socket and eventlistener to get rolls from the server
	def __init__(self):
		pygame.init

		#load images
		pin_images = [pygame.image.load('../assets/pin{}.png'.format(i)).convert() for i in [90,70,40,0]]
		ball_image = pygame.image.load('../assets/ball.png').convert()
		lane_image = pygame.image.load('../assets/lane.png').convert()

		game_window = pygame.display.set_mode((800, 600))

		reset_pins()
		while True: # main game loop
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == NEW_FRAME #@todo(jamie) have the scorer create a NEW_FRAME event after each frame
					reset_pins()
					pass #@todo(bumsik) have an eventlistener wait until we get the input

	def reset_pins():
		self.pins = []
		for i in range(10):
			y_pos = PIN_LOCATIONS[i][0]
			x_pos = PIN_LOCATIONS[i][0]
			self.pins.append(engine.Pin(x_pos, y_pos))

#notes from aaron http://inventwithpython.com/pygame/chapter2.html
#http://inventwithpython.com/pygame/chapter3.html

#wake me up at 8am i'mm be in quiet room
#dow hat you can until then
#jamie google 'bowling score kata' it will HELP YOU
#bumsik you're a great dev, it's been awesome working with you
#will you're awesome, if we were gays we'd probably be married by now or smth (no homo)