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
		x = magnitude * math.radians(math.cos(angle))
		y = magnitude * math.radians(math.sin(angle))
		return x,y

	def slope(x1, y1, x2, y2):
		return (y1-y2)/(x1-x2)

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
		force,clen = calculate_overlap(x1, y1, rad1, x2, y2, rad2)#clen is chord length
		force = force * physics_coefficent

		if x1 == x2:
			angle = 0 #@debug switch these
		elif y1 == y2:
			angle = 180 #might need to switch the 0 and 180, although this should be so rare that we dont notice this bug
		else:
			#how do i get this angle?
			angle = slope(x1,y2,x2,y2)
			angle = math.degrees(math.atan(slope))
		return force,angle

	def calculate_overlap(x0, y0, r0, x1, y1, r1)#from stackexchange https://math.stackexchange.com/questions/97850/get-the-size-of-an-area-defined-by-2-overlapping-circles
		rr0 = r0*r0;
		rr1 = r1*r1;
		c = Math.sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0));
		phi = (math.acos((rr0+(c*c)-rr1) / (2*r0*c)))*2;
		theta = (math.acos((rr1+(c*c)-rr0) / (2*r1*c)))*2;
		area1 = 0.5*theta*rr1 - 0.5*rr1*math.sin(theta);
		area2 = 0.5*phi*rr0 - 0.5*rr0*math.sin(phi);
		return area1 + area2,c

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
			imp_x = force_ * math.sin(math.radians(angle_)) #these two might be mixed up
			imp_y = force_ * math.cos(math.radians(angle_)) #@debug you should switch these


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