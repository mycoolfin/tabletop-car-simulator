from collections import deque
import numpy as np
import cv2
import time
import math

RED_MIN = np.array([172, 40, 40],np.uint8)
RED_MAX = np.array([180, 255, 210],np.uint8)
ORANGE_MIN = np.array([0, 50, 50],np.uint8)
ORANGE_MAX = np.array([20, 255, 255],np.uint8)
GREEN_MIN = np.array([50, 60, 60],np.uint8)
GREEN_MAX = np.array([60, 220, 220],np.uint8)
PINK_MIN = np.array([130, 40, 40],np.uint8)
PINK_MAX = np.array([180, 220, 220],np.uint8)
COLOUR_MIN = [PINK_MIN]
COLOUR_MAX = [PINK_MAX]
IDs = [10]


class CarTracker:
    def __init__(self):
        self.last_locs = [[-1,-1],[-1,-1],[-1,-1]]
        self.last_angle = [0,0,0]
        self.ticks = 0

    def findCar(self, image):
        pos = [-1,-1]
        scan_y = []
        y = 0
        while (y < 480):
            scan_value = cv2.countNonZero(image[y,0:640])
            if (scan_value > 0):
                if (len(scan_y) == 0):
                    pos[1] = y
                scan_y.append(scan_value)
            else:
                if (len(scan_y) > 0):
                    pos[1] += len(scan_y) // 2
                    break
            y = y + 1

        scan_x = []
        x = 0
        while (x < 640):
            scan_value = cv2.countNonZero(image[0:480,x])
            if (scan_value > 0):
                if (len(scan_x) == 0):
                    pos[0] = x
                scan_x.append(scan_value)
            else:
                if (len(scan_x) > 0):
                    pos[0] += len(scan_x) // 2
                    break
            x = x + 1
        return pos

    def track_cars(self, image):
        car_locations = []
        index = 0
        while (index < 1):
            thresh = cv2.inRange(cv2.cvtColor(image,cv2.COLOR_BGR2HSV), COLOUR_MIN[index], COLOUR_MAX[index])
            cpos = self.findCar(thresh)
            if (self.ticks > 10):
                dx = cpos[0] - self.last_locs[index][0]
                dy = cpos[1] - self.last_locs[index][1]
                theta = 0
                if (dx != 0):
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
                self.last_angle[index] = theta
                self.last_locs[index] = cpos
                self.ticks = 0

            dict = {"ID": index, "position": cpos, "orientation": self.last_angle[index]}
            car_locations.append(dict)
            index += 1

        self.ticks+=1
        return car_locations
