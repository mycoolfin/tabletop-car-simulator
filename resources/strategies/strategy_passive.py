"""
PASSIVE

Agent will navigate waypoints slowly,
stopping if a collision is imminent.
"""

import math, time

def make_decision(self):
	# Give self access to information about other vehicles.
	if "vehicles" not in self.worldKnowledge.keys():
		self.worldKnowledge['vehicles'] = []
		return

	# If we don't know where we are, stop.
	if self.vehicle.position == (None, None) or self.vehicle.orientation == None:
		self.vehicle.stop()
		return

	# Check positions of other cars.
	for vehicle in self.worldKnowledge['vehicles']:
		if vehicle.owner.ID == self.vehicle.owner.ID or vehicle.position == (None, None):
			continue
		# Get distances to other cars.
		xDist = vehicle.position[0] - self.vehicle.position[0]
		yDist = vehicle.position[1] - self.vehicle.position[1]
		dist = math.hypot(xDist, yDist)
		# If we are too close to another car, stop and complain.
		if dist < 50:
			self.vehicle.stop()
			self.vehicle.horn_on()
			self.vehicle.headlights_on()
			time.sleep(1)
			self.vehicle.horn_off()
			self.vehicle.headlights_off()
			return

	# Find waypoint vector info
	(wp_dist, wp_angle) = self.get_vector_to_waypoint()

	if (wp_dist < 50): # If we are close enough to our waypoint, set our sights on the next one
		self.set_waypoint_index(self.get_waypoint_index() + 1)
	else: # Drive slowly towards current waypoint. Slow down drastically if we are not directed towards the waypoint
		speed = 8
		car_angle = self.vehicle.get_orientation()
		a = int(math.fabs(car_angle - wp_angle))
		if (a > 180):
			a = 360 - a
			if (car_angle < wp_angle):
				da = -a
			else:
				da = a
		else:
			if (car_angle < wp_angle):
				da = a
			else:
				da = -a
		self.vehicle.set_angle(da // 2)
		self.vehicle.set_speed(speed)
