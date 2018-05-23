"""
Functionality Test Strategy File
"""

import math

if not 'ticks' in self.worldKnowledge:
    self.worldKnowledge['ticks'] = 0


if (self.worldKnowledge['ticks'] > 40):
    self.aim_speed(5)

if (self.worldKnowledge['ticks'] > 60):
    self.vehicle.set_speed(0)

self.worldKnowledge['ticks'] += 1


