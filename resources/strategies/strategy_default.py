"""
Controlled default strategy.

Aim to slowly navigate waypoints in an orderly fashion with some basic error checks
"""

# If we don't know where we are, STOP
if self.vehicle.position == (None, None) or self.vehicle.orientation == None:
	self.vehicle.stop()


else:
	# Find waypoint vector info
	(wp_dist, wp_angle) = self.get_vector_to_waypoint()

	print("\n")
	print("Waypoint: " + str(self.worldKnowledge['waypoints'][self.get_waypoint_index()]))
	print(self.worldKnowledge['waypoint_index'])
	print("Position: " + str(self.vehicle.position))
	print("WP Dista: " + str(wp_dist))
	print("WP Angle: " + str(wp_angle))
	print("\n")

	# If we are close enough to our waypoint, set our sights on the next one
	if (wp_dist < 50):
		self.set_waypoint_index(self.get_waypoint_index() + 1)

	# Drive slowly towards current waypoint. Slow down drastically if we are not directed towards the waypoint
	else:
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
