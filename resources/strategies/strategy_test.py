"""
Functionality Test Strategy File
storage[0] = tick timer
"""

if not 'ticks' in self.worldKnowledge:
    self.worldKnowledge['ticks'] = 0

if (self.worldKnowledge['ticks'] > 50):
    self.aim_speed(0)
    self.aim_angle(0)
else:
    if (self.worldKnowledge['ticks'] < 35):
        self.aim_speed(20)
        self.aim_angle(0)
    else:
        self.aim_speed(0)
        self.aim_angle(0)
    self.worldKnowledge['ticks'] += 1


        
