#!/usr/bin/env python3
import math

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

	knock_resistance = 10
	height = 15
	def __init__(self, position):
		self.position = position
		self.tip = 1 #1 = standing up, 0 = horizontal
		self.angle = 0 	#WE ARE USING DEGREES, NOT RADIANS
						#0 is pointed NORTH
	def impact(force, angle):
		pass #@todo(someone) code this


class Lane:
	"""
	A bowling lane with pins, and a ball.
	"""
	ball_mass = 10 #this is an @arbitrary number, adjust as needed

	def __init__(self):
		pins = self.ten_pins()

	def ten_pins():
		return [Pin(PIN_LOCATIONS[i]) for i in range(10)] #pin indicies are 1-10, because thats how bowling does it

	def roll_ball(ball_x, ball_vel, ball_spin, ball_angle):
		'''
		@params:
			ball_x is a float between 9.25 and 50.75 inclusive
			ball_vel is how fast the ball is rolling
			ball_spin is the spin on the ball (to make it curve) (maybe don't use this)
			ball_angle is the angle that the ball is going in
		'''
		pass #@todo(someone) code this

class BowlingGame:
	"""
	The game!
	"""
	#do we need this?
	#@todo(aaron) answer the above question