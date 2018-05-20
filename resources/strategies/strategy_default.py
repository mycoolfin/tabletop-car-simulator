"""
Controlled default strategy.

Aim to slowly navigate waypoints in an orderly fashion with some basic error checks
"""



#If we don't know where we are, STOP
if self.vehicle.position == (None, None):
    self.vehicle.noneTicks += 1
    if (self.vehicle.noneTicks >= 10):
        self.vehicle.stop()


else:
    self.vehicle.noneTicks = 0
    #Find waypoint vector info
    (wp_dist,wp_angle) = self.vehicle.get_vector_to_waypoint()

    print("\n")
    print("Waypoint: " + str(self.worldKnowledge['waypoints'][self.vehicle.get_waypoint_index()]))
    print("Position: " + str(self.vehicle.position))
    print("WP Dista: " + str(wp_dist))
    print("WP Angle: " + str(wp_angle))
    print("\n")
    
    #If we are close enough to our waypoint, set our sights on the next one
    if (wp_dist < 10):
        self.vehicle.set_waypoint_index(self.vehicle.get_waypoint_index()+1)
            
    #Drive slowly towards current waypoint. Slow down drastically if we are not directed towards the waypoint
    else:
        fast_speed = 20
        slow_speed = 5
        a_thresh = 10
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
        self.vehicle.set_angle(da)
        if (a > a_thresh):
            self.vehicle.set_speed(slow_speed)
        else:
            self.vehicle.set_speed(fast_speed)


        
