"""
Controlled default strategy.

Aim to slowly navigate waypoints in an orderly fashion with some basic error checks
"""

#If we don't know where we are, STOP
if self.vehicle.position == (None, None):
    self.vehicle.stop()
	return
	
#If we are close enough to our waypoint, set our sights on the next one
if (self.vehicle.get_distance_to_waypoint() < 10):
	self.vehicle.set_waypoint_index(self,self.vehicle.get_waypoint_index()+1)
	
#Drive slowly towards current waypoint. Slow down drastically if we are not directed towards the waypoint
else:
	fast_speed = 20
	slow_speed = 5
	a_thresh = 10
	car_angle = self.get_orientation()
	waypoint_angle = self.get_bearing_to_waypoint()
	a = math.abs(car_angle - waypoint_angle)
	if (a > 180):
		a = 360 - a
		if (car_angle < waypoint_angle):
			da = -a
		else:
			da = a
	else:
		if (car_angle < waypoint_angle):
			da = a
		else:
			da = -a
	
	self.vehicle.set_angle(da)
	if (a > a_thresh):
		self.vehicle.set_speed(slow_speed)
	else:
		self.vehicle.set_speed(fast_speed)
