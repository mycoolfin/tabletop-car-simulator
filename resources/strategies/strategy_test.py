"""
Functionality Test Strategy File
"""
if (self.vehicle.storage[0] > 100):
    self.vehicle.stop()
else:
    if (self.vehicle.storage[0] < 50):
        self.vehicle.aim_speed(50)
    else:
        self.vehicle.aim_speed(0)
    self.vehicle.storage[0] += 1


        
