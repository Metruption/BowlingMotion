#!/usr/bin/env python3
import math
#distance units are in inches
#weight units are in kilos

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
#the distance between pin rows is sqrt(108)inches which is ~10.4 inches
#pins are 12 inches apart and form an eqilateral triangle
#see this page for info on bowling lane stuff:
# http://www.courtdimensions.net/bowling-lane/index.php

class Pin:
	"""These poor guys get knocked around a lot."""

	radius = 2.25 #our pins are going to basically be cylinders
	mass = 1.5 #kilos
	height = 15 #inches
	def __init__(self, pos):
		self.xpos, self.ypos = pos[1], pos[1]
		self.tip = 1 #1 = standing up, 0 = horizontal
		self.angle = 0 	#WE ARE USING DEGREES, NOT RADIANS
						#0 is pointed NORTH
	def impact(force, angle):
		pass #@todo(someone) code this


class Lane:
	"""
	A bowling lane with pins, and a ball.
	The 'physics engine'
	"""
	ball_mass = 10 #this is an @arbitrary number, adjust as needed
	ball_radius = 4.25

	def __init__(self):
		self.start_frame()

	def start_frame():
		self.pins = self.ten_pins()

	def ten_pins():
		return [Pin(PIN_LOCATIONS[i]) for i in range(10)] #pin indicies are 1-10, because thats how bowling does it

	def distance(x1,y1,x2,y2):
		'''
		@params:
			x1 and y1 are the (x,y) coords of one points
			x2 and y2 are the (x,y) coords of a second point

		returns the distance between the two points
		'''
		return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


	def roll_ball(ball_x, ball_vel, ball_spin=None, ball_angle):
		def split_vel():
			ball_xvel = '@todo(someone) code this' #not aaron, he doesnt know trig
			ball_yvel = '@todo(someone) code this' #not arrow he doesnt know trig

		def update_bal_pos():
			ball_x = ball_x + ball_xvel
			ball_y = ball_y + ball_yvel
		'''
		@params:
			ball_x is a float between 9.25 and 50.75 inclusive (you cant start out in the gutter)
			ball_vel is how fast the ball is rolling
			ball_spin is the spin on the ball (to make it curve) (maybe don't use this)
			ball_angle is the angle that the ball is going in
		'''
		ball_y = 0.0
		pins_knocked = []

		continue_simulation = True
		while continue_simulation:
			#render_image() ????
			split_vel()
			update_bal_pos()

			if ball_y > 50.75 or ball_y < 9.25: #check if the ball is in the gutters
				continue_simulation = False
				#this is a gutter ball!

			pin_distances = [distance(ball_x, ball_y, pin.xpow, pin.ypos) for pin in pins]
			for pin_distance in pin_distances:
				if pin_distance < ball_radius + Pin.radius:
					#@todo(aaron): figure out how to make the ball impact the pin

class BowlingGame:
	"""
	The game!
	"""
	#do we need this?
	#@todo(aaron) answer the above question
	#the answer is yes!
	#it has a bowling lane
	#it keeps track of scoring