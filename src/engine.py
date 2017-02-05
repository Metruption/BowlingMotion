#!/usr/bin/env/python3
import math
import mathutil

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


	def detect_collision(target):
		'''
		@params:
			target is an Actor

		returns true if self is colliding with target, false otherwise
		two objects are considered to be colliding if they attempt to occupy the same space
		two objects are NOT considered to be colliding if they are tangent
		'''
		safe_zone = self.radius + target.radius
		distance = mathutil.distance(self.xpos, self.ypos, target.xpos, target.ypos)
		return safe_zone > distance


	def resolve_collision(target):
		'''
		@params:
			target is an Actor

		resolves a collision between self and target by impacting them
		they are impacted harder if they have more collision
		if there is no collision then this returns False
		otherwise it returns True
		'''
		if not self.detect_collision(target): return False

		#@todo(aaron):figure out how to do this properly
		radii_ratio = self.radius / target.radius

		distance = mathutil.distance(self.xpos, self.ypos, target.xpos, target.ypos)
		radii_sum = self.radius + target.radius
		overlap_size = radii_sum - distance
		impact_total = radii_ratio * overlap_size #this code approximates the impacts, and will probably not be satisfactory

		impact_angle = math.atan(slope(self.xpos, self.ypos, target.xpos, target.ypos))
		x_impact = impact_total * math.cos(impact_angle)
		y_impact = impact_total * math.sin(impact_angle)
		#the angle is correct (although you might need to switch the cos and sin)

		#obeying newton's third law
		self.impact(x_impact/2, y_impact/2)
		target.impact(-x_impact/2, -y_impact/2)

		return True



class Pin(Actor):
	def __init__(self, radius2=2.5, mass=1.5, frict=5, xpos, ypos):
		Actor.__init__(radius, mass, frict, xpos, ypos)
		standing = True

	def impact(xforce, yforce):
		Actor.impact(xforce, yforce)
		if math.sqrt(xforce**2 + yforce**2) > mass:
			standing = False

class Ball(Actor): #yeah this is just a wrapper...
	def __init__(self, radius=4.25, mass=10, frict=1.1, xpos=30, ypos=):
		Actor.__init__(radius, mass, frict, xpos, ypos)