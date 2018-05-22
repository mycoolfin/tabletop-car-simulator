"""
Functionality Test Strategy File
storage[0] = tick timer
"""
if (self.vehicle.storage[0] > 50):
    self.vehicle.aim_speed(0)
    self.vehicle.aim_angle(0)
else:
    if (self.vehicle.storage[0] < 35):
        self.vehicle.aim_speed(20)
        self.vehicle.aim_angle(0)
    else:
        self.vehicle.aim_speed(0)
        self.vehicle.aim_angle(0)
    self.vehicle.storage[0] += 1


        
