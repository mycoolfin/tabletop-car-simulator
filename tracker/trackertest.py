from camera import Camera
import cv2
import numpy as np
import time

# RED_MIN = np.array([170, 40, 40],np.uint8)
# RED_MAX = np.array([180, 150, 150],np.uint8)
# ORANGE_MIN = np.array([2, 70, 90],np.uint8)
# ORANGE_MAX = np.array([8, 200, 200],np.uint8)
# GREEN_MIN = np.array([35, 60, 60],np.uint8)
# GREEN_MAX = np.array([80, 220, 220],np.uint8)
# PINK_MIN = np.array([150, 60, 60],np.uint8)
# PINK_MAX = np.array([165, 220, 220],np.uint8)

GREEN_MIN = np.array([34, 60, 60], np.uint8)
GREEN_MAX = np.array([60, 220, 220], np.uint8)
PINK_MIN = np.array([130, 40, 40], np.uint8)
PINK_MAX = np.array([180, 220, 220], np.uint8)


def findCar(image):
	pos = [-1, -1]
	scan_y = []
	y = 0

	while (y < 480):
		scan_value = cv2.countNonZero(image[y, 0:640])
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
		scan_value = cv2.countNonZero(image[0:480, x])
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


def main():
	cam = Camera()
	# frame = cv2.cvtColor(cam.get_frame(),cv2.COLOR_BGR2HSV)
	cv2.imwrite("hues.png", cam.get_frame())
	# thresh = cv2.inRange(frame, PINK_MIN, PINK_MAX)
	# cv2.imshow('thresh',thresh)
	# print(findCar(thresh))
	# cv2.waitKey(3000)
	# thresh = cv2.inRange(frame, GREEN_MIN, GREEN_MAX)
	# cv2.imshow('thresh',thresh)
	# print(findCar(thresh))
	# cv2.waitKey(3000)


main()
