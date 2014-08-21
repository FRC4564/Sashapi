#import maestro

# For motor controllers, servo speed setting dampens acceleration (acts like inertia).
# Higher values will reduce inertia (try values around 50 to 100) 
INERTIA = 200
#

class DriveTrain:
        # Init drive train, passing maestro controller obj, and channel
        # numbers for the motor servos Left and Right
	def __init__(self, maestro,chLeft,chRight):
		self.maestro = maestro
		self.chRight = chRight
		self.chLeft = chLeft
		# Init motor accel/speed params
		self.maestro.setAccel(chRight,0)
		self.maestro.setAccel(chLeft,0)
		self.maestro.setSpeed(chRight,INERTIA)
		self.maestro.setSpeed(chLeft,INERTIA)
		# Right motor min/center/max vals
		self.minR = 2760
		self.centerR = 6000
		self.maxR = 9300
		# Left motor min/center/max vals
		self.minL = 2760
		self.centerL = 6000
		self.maxL = 9300

	# Mix joystick inputs into motor L/R mixes
	def arcadeMix(self, joyX, joyY):
		r = -1 * joyX
		l = joyY
		v = (1 - abs(r)) * l + l
		w = (1 - abs(l)) * r + r
		motorR = -(v + w) / 2  
		motorL = (v - w) / 2
		return (motorR, motorL)

	# Scale motor speeds (-1 to 1) to maestro servo target values
	def maestroScale(self, motorR, motorL):
		if (motorR >= 0) :
			r = int(self.centerR + (self.maxR - self.centerR) * motorR)
		else:
			r = int(self.centerR + (self.centerR - self.minR) * motorR)
		if (motorL >= 0) :
			l = int(self.centerL + (self.maxL - self.centerL) * motorL)
		else:
			l = int(self.centerL + (self.centerL - self.minL) * motorL)
		return (r, l)

	# Blend X and Y joystick inputs for arcade drive and set servo
	# output to drive motor controllers
	def drive(self, joyX, joyY):
		(motorR, motorL) = self.arcadeMix(joyX, joyY)
		(servoR, servoL) = self.maestroScale(motorR, motorL)
		#print "Target R = ",servoR
		self.maestro.setTarget(self.chRight, servoR)
		self.maestro.setTarget(self.chLeft, servoL)

	# Set both motors to stopped (center) position
	def stop(self):
		self.maestro.setTarget(self.chRight, self.centerR)
		self.maestro.setTarget(self.chLeft, self.centerL)

	# Close should be used when shutting down Drive object
	def close(self):
		self.stop()
