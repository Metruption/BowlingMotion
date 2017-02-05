#!/usr/bin/env/python3
import math

def main():
	print("Not for human consumption. Please evacuate the premises.")

if name == '__main__':
	main()

def distance(x1,y1,x2,y2):
	'''
	@params:
		x1 and y1 are the (x,y) coords of one points
		x2 and y2 are the (x,y) coords of a second point
	
	returns the distance between the two points
	'''
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)