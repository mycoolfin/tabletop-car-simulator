import time
import math

from controller.zenwheels.protocol import *


class Vehicle:
    def __init__(self, owner):
        # Vehicle properties.
        self.owner = owner
        self.waypoint_index = None	# Keeps track of waypoint progression.
        self.position = None, None  # World coordinates (x, y).
        self.orientation = None  # Degrees clockwise from north.
        self.dimensions = None, None  # Size and shape (width, length).
        self.max_speed = None
        self.max_acceleration = None
        self.max_deceleration = None
        self.max_turn = None
        self.max_turn_change = None

        # Vehicle state.
        self.current_speed = None
        self.current_angle = None
        self.horn_active = False
        self.headlights_active = False
        self.left_signal_active = False
        self.right_signal_active = False
        self.noneTicks = 0  # Used to remember how many times we have recieved no information

        # List of commands to be sent to the corresponding ZenWheels car.
        self.command_queue = {}

    def set_speed(self, speed):
        if speed >= 0: # Forwards.
            if speed > 63: # Maximum.
                speed = 63
            self.queueCommand(bytes([THROTTLE, speed]))
        else: # Backwards.
            if speed < -64: # Maximum.
                speed = 64
            else:
                speed = 128 + speed
            self.queueCommand(bytes([THROTTLE, speed]))

    def set_angle(self, angle):
        if angle >= 0: # Steering right.
            if angle > 63: # Maximum.
                angle = 63
            self.queueCommand(bytes([STEERING, angle]))
        else: # Steering left.
            if angle < -64: # Maximum.
                angle = 64
            else:
                angle = 128 + angle
            self.queueCommand(bytes([STEERING, angle]))

    #Return Distance and Angle to current waypoint. Angle must be degrees clockwise from north
    def get_vector_to_waypoint(self):
        if (self.position[0] != None and self.position[1] != None):
             if (self.waypoint_index != None):
                if (self.owner.worldKnowledge['waypoints'] != []):
                    x1 = self.position[0]
                    y1 = self.position[1]
                    x2 = self.owner.worldKnowledge['waypoints'][self.waypoint_index][0]
                    y2 = self.owner.worldKnowledge['waypoints'][self.waypoint_index][1]
                    dx = x2 - x1
                    dy = y2 - y1
                    dist = int(math.sqrt(dx*dx + dy*dy))

                    theta = math.atan(dy/dx)*(180/math.pi)
                    if (dx == 0):
                        if (dy <= 0):
                            theta = 0
                        else:
                            theta = 180
                    elif (dy == 0):
                        if (dx < 0):
                            theta = 90
                        else:
                            theta = 270
                    elif (dx > 0 and dy > 0):
                        theta = theta + 90
                    elif (dx > 0 and dy < 0):
                        theta = theta + 90
                    elif (dx < 0 and dy > 0):
                        theta = theta + 270
                    elif (dx < 0 and dy < 0):
                        theta = theta + 270

                    return (dist,theta)
        return (None,None)

    #Return current waypoint index
    def get_waypoint_index(self):
        return self.waypoint_index

    #Set current waypoint index
    def set_waypoint_index(self, wp):
        mmax = len(self.owner.worldKnowledge['waypoints']) - 1
        if (wp > mmax):
            wp = mmax
        if (wp < 0):
            wp = 0
        self.waypoint_index = wp

    def get_orientation(self):
        return self.orientation
	
    def stop(self):
        self.queueCommand(bytes([THROTTLE, 0]))

    def horn_on(self):
        if self.horn_active == False:
            self.queueCommand(bytes([HORN, HORN_ON]))
            self.horn_active = True
    def horn_off(self):
        if self.horn_active == True:
            self.queueCommand(bytes([HORN, HORN_OFF]))
            self.horn_active = False

    def headlights_on(self):
        if self.headlights_active == False:
            self.queueCommand(bytes([HEADLIGHT, HEADLIGHT_BRIGHT]))
            self.headlights_active = True

    def headlights_off(self):
        if self.headlights_active == True:
            self.queueCommand(bytes([HEADLIGHT, HEADLIGHT_OFF]))
            self.headlights_active = False

    def left_signal_on(self):
        if self.left_signal_active == False:
            self.queueCommand(bytes([LEFT_SIGNAL, SIGNAL_FRONT_BRIGHT]))
            self.left_signal_active = True

    def left_signal_off(self):
        if self.left_signal_active == True:
            self.queueCommand(bytes([LEFT_SIGNAL, SIGNAL_OFF]))
            self.left_signal_active = False

    def right_signal_on(self):
        if self.right_signal_active == False:
            self.queueCommand(bytes([RIGHT_SIGNAL, SIGNAL_FRONT_BRIGHT]))
            self.right_signal_active = True

    def right_signal_off(self):
        if self.right_signal_active == True:
            self.queueCommand(bytes([RIGHT_SIGNAL, SIGNAL_OFF]))
            self.right_signal_active = False

    def queueCommand(self, command):
        self.command_queue[command] = int(round(time.time()*1000)) # Append time of queueing in milliseconds.


class Car(Vehicle):
    def __init__(self, owner):
        Vehicle.__init__(self, owner)
        self.max_speed = 50
        self.dimensions = (35,60)

class Truck(Vehicle):
    def __init__(self, owner):
        Vehicle.__init__(self, owner)
        self.max_speed = 40
        self.dimensions = (40,90)

class Motorcycle(Vehicle):
    def __init__(self, owner):
        Vehicle.__init__(self, owner)
        self.max_speed = 60
        self.dimensions = (15,30)

class Bicycle(Vehicle):
    def __init__(self, owner):
        Vehicle.__init__(self, owner)
        self.max_speed = 20
        self.dimensions = (8,25)

