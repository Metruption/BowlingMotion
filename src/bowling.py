#!/usr/bin/env python3
import math
#distance units are in inches
#weight units are in kilos

#HERE BE DRAGONS
#this is hackathon code
#hackathon code is rarely good code
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
	tippyness = mass + 0 #the + n is arbitrary
	height = 15 #inches
	def __init__(self, pos, id_):
		self.xpos, self.ypos = pos[1], pos[1]
		self.id = id_
		self.xvel = 0
		self.yvel = 0
		self.standing = True
		self.angle = 0 	#WE ARE USING DEGREES, NOT RADIANS
						#0 is pointed NORTH
	def impact(force, angle):
		dx,dy = split_vector(force,angle)
		self.xvel = dx
		self.yvel = dy
		if force > self.tippyness:
			self.standing = False

class Lane:
	"""
	A bowling lane with pins, and a ball.
	The 'physics engine'
	this is becoming a mangled ball class, but i REFUSE to trash it!
	"""
	physics_coefficent = 1 #this is an @arbitrary number, adjust as needed
	ball_mass = 10 #this is an @arbitrary number, adjust as needed
	ball_radius = 4.25

	def __init__(self):
		self.start_frame()

	def start_frame():
		self.pins = self.ten_pins()

	def ten_pins():
		return [Pin(PIN_LOCATIONS[i], i+1) for i in range(10)] #pin ids are 1-10, because thats how they are labeled in bowling

	def distance(x1,y1,x2,y2):
		'''
		@params:
			x1 and y1 are the (x,y) coords of one points
			x2 and y2 are the (x,y) coords of a second point

		returns the distance between the two points
		'''
		return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

	def split_vector(angle, magnitude):#@debug, may need to switch these
		x = magnitude * math.cos(angle)
		y = magnitude * math.sin(angle)
		return x,y

	def collide_circles(rad1, x1, y1, rad2, x2, y2):
		'''
		@params:
			rad1 is radius of circle1
			x1 is x coord of circle1's center
			y1 is y coord of circle1's center
			same for rad2, x2, y2
		
		returns two
		first value is the force impacted on the circles
		second value is the angle of the force impacted on the second circle
		'''
		intersect_len = abs(distance(x1,y1,x2,y2) - rad1 - rad2)
		radrat = rad1/rad2
		thezone = intersect_len * radrat
		force = thezone * physics_coefficent

		if x1 == x2:
			angle = 0 #@debug switch these
		elif y1 == y2:
			angle = 180 #might need to switch the 0 and 180, although this should be so rare that we dont notice this bug
		else:
			#how do i get this angle?
			angle = "@todo(aaron) code this"
		return force,angle

	def unfuck_angle(angle_): #i later realized I can just do -force instead FUCK
		angle_ = angle_ + 180
		if angle_ >= 360:
			angle_ = angle_ - 360
		return angle_


	def roll_ball(ball_x, ball_vel, ball_spin=None, ball_angle):
		def split_vel():
			dx,dy = split_vector(force_,angle_)
			ball_xvel = dx
			ball_yvel = dy

		def update_bal_pos():
			ball_x = ball_x + ball_xvel
			ball_y = ball_y + ball_yvel


		def impact_ball(force, angle):
			'''
			@params:
				ball_x is a float between 9.25 and 50.75 inclusive (you cant start out in the gutter)
				ball_vel is how fast the ball is rolling
				ball_spin is the spin on the ball (to make it curve) (maybe don't use this)
				ball_angle is the angle that the ball is going in

			returns the number of pins knocked down
			'''
			imp_x = force_ * math.sin(angle_) #these two might be mixed up
			imp_y = force_ * math.cos(angle_) #@debug you should switch these


		ball_y = 0.0
		pins_knocked = 0

		continue_simulation = True
		physics = False
		while continue_simulation:
			#render_image() ????
			split_vel()
			update_bal_pos()

			if ball_x > 50.75 or ball_x < 9.25: #check if the ball is in the gutters
				continue_simulation = False
				#this is a gutter ball!

			physics = ball_y >= 720 - ball_radius - Pin.radius

			if physics:
				for pin in pins: #first we detect collision for the pins
					force, angle = collide_circles(ball_radius, ball_x, ball_y, pin.radius, pin.x, pin.y)
					pin.impact(force, angle)
					ball_angle = self.unfuck_angle(angle)
					impact_ball(force, ball_angle)
					for pin2 in pins:
						if pin is pin2: #don't try to collide a pin with itself
							continue

						force, angle = collide_circles(pin.radius, pin.x, pin.y, pin2.radius, pin2.x, pin2.y)
						pin2.impact(force, angle)
						pin.impact(force, self.unfuck_angle(angle))

				for pin in pins: #then we move the pins
					pin.x = pin.x + pin.xvel
					pin.y = pin.y + pin.yvel


		#at this point the bowling simulation is done
		for pin in pins:
			if not pin.standing:
				pins.remove(pin)
				pins_knocked = pins_knocked + 1

		return pins_knocked

class BowlingGame:
	"""
	The game!
	"""
	#do we need this?
	#the answer is yes!
	#it has a bowling lane
	#it keeps track of scoring
	#also it probably handles rendering...?