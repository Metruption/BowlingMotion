#!/usr/bin/env/python3
import math

def main():
	print("Not for human consumption. Please evacuate the premises.")

if __name__ == '__main__':
	main()

def distance(x1,y1,x2,y2):
	'''
	@params:
		x1 and y1 are the (x,y) coords of one points
		x2 and y2 are the (x,y) coords of a second point
	
	returns the distance between the two points
	'''
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def slope(x1, y1, x2, y2):
	'''
	@params:
		x1 and y1 are the (x,y) coords of one points
		x2 and y2 are the (x,y) coords of a second point

	returns the slope of a line drawn between the two points
	'''
	return (y1 - y2)/(x1 - x2)

def between(num, min_, max_):
	'''
	@params:
		num is a real number
		min_ is a real number
		max_ is a real number which should be larger than min_

	returns true if number is between min_ and max_
	'''
	return num >= min_ and num <= max_