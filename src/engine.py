#!/usr/bin/env/python3
import math

def main():
	print("Not for human consumption. Please evacuate the premises.")

if name == '__main__':
	main()

class Actor:
	"""These poor guys get knocked around a lot."""

	radius = 2.25 #our pins are going to basically be cylinders
	mass = 1.5 #kilos
	height = 15 #inches
	def __init__(self, radius, mass, frict, xpos, ypos):
		self.xvel = 0
		self.yvel = 0
		self.xpos = xpos
		self.ypos = ypos
		self.radius = radius
		self.mass = mass
		self.frict = frict

	def impact(xforce, yforce):
		dx = xforce / self.mass
		dy = yforce / self.mass
		self.xvel += dx
		self.yvel += dy

class Pin(Actor):
	def __init__(self, radius, mass, frict, xpos, ypos):
		Actor.__init__(radius, mass, frict, xpos, ypos)
		standing = True

	def impact(xforce, yforce):
		Actor.impact(xforce, yforce)
		if math.sqrt(xforce**2 + yforce**2) > mass:
			standing = false

class Ball(Actor): #yeah this is just a wrapper...
	def __init__(self, radius, mass, frict, xpos, ypos):
		Actor.__init__(radius, mass, frict, xpos, ypos)

class Lane: