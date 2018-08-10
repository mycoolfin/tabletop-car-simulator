import numpy as np
import cv2
import time
import math

RED_ID = "72"
RED_MIN = np.array([0, 150, 0], np.uint8)
RED_MAX = np.array([4, 255, 150], np.uint8)
ORANGE_ID = "45"
ORANGE_MIN = np.array([5, 100, 150], np.uint8)
ORANGE_MAX = np.array([10, 255, 255], np.uint8)
GREEN_ID = "61"
GREEN_MIN = np.array([35, 70, 50], np.uint8)
GREEN_MAX = np.array([45, 200, 255], np.uint8)
PINK_ID = "10"
PINK_MIN = np.array([160, 70, 50], np.uint8)
PINK_MAX = np.array([180, 200, 255], np.uint8)

cars_info = [[RED_ID, RED_MIN, RED_MAX],
			 [ORANGE_ID, ORANGE_MIN, ORANGE_MAX],
			 [GREEN_ID, GREEN_MIN, GREEN_MAX],
			 [PINK_ID, PINK_MIN, PINK_MAX]]


class CarTracker:
	def __init__(self):
		self.last_locations = {}
		self.last_angles = {}
		self.last_times = {}

	def track_cars(self, image):
		start = time.time()
		car_locations = []
		hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		for car_info in cars_info:
			hue_mask = cv2.inRange(hsv_img, car_info[1], car_info[2])
			dilated = cv2.dilate(hue_mask, np.ones((5,5), np.uint8))
			_, contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

			potentialMatches = []
			for c in contours:
				area = cv2.contourArea(c)
				perimeter = cv2.arcLength(c, True)
				ratio = area / perimeter
				if area > 300 and area < 800 and ratio > 3.5:
					potentialMatches.append(c)
			if not potentialMatches:
				continue
			bestMatch = max(potentialMatches, key=cv2.contourArea)
			moments = cv2.moments(bestMatch)
			cx = int(moments['m10'] / moments['m00'])
			cy = int(moments['m01'] / moments['m00'])

			car_id = car_info[0]
			car_position = (cx, cy)

			current_time = time.time()
			if not car_id in self.last_locations.keys():
				self.last_locations[car_id] = car_position
				self.last_angles[car_id] = 0
				self.last_times[car_id] = time.time()

			if ((current_time - self.last_times[car_id]) * 1000 > 500):
				dx = car_position[0] - self.last_locations[car_id][0]
				dy = car_position[1] - self.last_locations[car_id][1]

				# Filter out small dy, dx values.
				if abs(dx) < 5 and abs(dy) < 5:
					theta = self.last_angles[car_id]
				else:
					theta = 0
					if (dx != 0):
						theta = math.atan(dy / dx) * (180 / math.pi)
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

					# Filter out 180 degree flips.
					if self.last_angles[car_id] is not None:
						diff = abs(theta - self.last_angles[car_id])
						if diff > 170 and diff < 190:
							# Ignore flip.
							theta = self.last_angles[car_id]


				self.last_times[car_id] = current_time
				self.last_angles[car_id] = int(theta)
				self.last_locations[car_id] = car_position

			car_locations.append({"ID": car_id, "position": car_position, "orientation": self.last_angles[car_id]})

		end = time.time()
		ms = str(int((end-start)*1000)) + " ms"
		print(ms)
		if car_locations:
			for car in car_locations:
				print("-------------------------------------")
				print("Agent " + str(car['ID']))
				print("Position: " + str(car['position']))
				print("Orientation: " + str(car['orientation']))
				print("-------------------------------------")
				print("")
		else:
			print("No cars found.")
		print("")
		return car_locations