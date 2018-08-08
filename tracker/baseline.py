import numpy as np
import cv2
import time
import math
from camera import Camera
from server import Server
from calibrator import Calibrator

ORANGE_MIN = np.array([0, 50, 50],np.uint8)
ORANGE_MAX = np.array([8, 255, 255],np.uint8)
RED_MIN = np.array([172, 50, 50],np.uint8)
RED_MAX = np.array([180, 255, 210],np.uint8)
GREEN_MIN = np.array([50, 50, 50],np.uint8)
GREEN_MAX = np.array([70, 255, 255],np.uint8)
PINK_MIN = np.array([160, 50, 50],np.uint8)
PINK_MAX = np.array([170, 255, 255],np.uint8)


class BaselineTracker():
	perspective_transform = None
	def __init__(self):
		self.background = None
	def track_cars(self, image):
		if self.background is None:
			print("ERROR: Must provide background image first.")
			return None

		car_locations = []

		# Step 1: Segment foreground from background.
		bg_img = self.background.copy()
		bg_gray = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		frame_diff = cv2.absdiff(gray, bg_gray)
		_, thresh = cv2.threshold(frame_diff, 20, 255, cv2.THRESH_BINARY)
		fg_img = cv2.bitwise_and(image, image, mask=thresh)

		# Step 2: Segment cars from foreground image.
		hsv_img = cv2.cvtColor(fg_img, cv2.COLOR_BGR2HSV)
		orange = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
		red = cv2.inRange(hsv_img, RED_MIN, RED_MAX)
		green = cv2.inRange(hsv_img, GREEN_MIN, GREEN_MAX)
		pink = cv2.inRange(hsv_img, PINK_MIN, PINK_MAX)

		kernel = np.ones((5, 5), np.uint8)
		orange_closed = cv2.morphologyEx(orange, cv2.MORPH_CLOSE, kernel)
		red_closed = cv2.morphologyEx(red, cv2.MORPH_CLOSE, kernel)
		green_closed = cv2.morphologyEx(green, cv2.MORPH_CLOSE, kernel)
		pink_closed = cv2.morphologyEx(pink, cv2.MORPH_CLOSE, kernel)

		_, orange_contours, _ = cv2.findContours(orange_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		_, red_contours, _ = cv2.findContours(red_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		_, green_contours, _ = cv2.findContours(green_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		_, pink_contours, _ = cv2.findContours(pink_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

		infoList = [(orange_closed, orange_contours, (0, 136, 255)),
					(red_closed, red_contours, (0, 0, 255)),
					(green_closed, green_contours, (0, 255, 0)),
					(pink_closed, pink_contours, (144, 0, 255))]
		for closed, contours, colour in infoList:
			if len(contours) > 0:
				# TODO: We know how big the cars should be - use this knowledge to filter bad boxes.
				c = max(contours, key=cv2.contourArea)

				boundingBox = cv2.boundingRect(c)
				x, y, w, h = boundingBox
				cv2.rectangle(image, (x, y), (x + w, y + h), colour, 4)

				#car_locations.append({"ID": index, "position": worldPosition, "orientation": angle})


		cv2.imshow("background", bg_img)
		cv2.imshow("fg", fg_img)
		cv2.imshow("final", image)

		cv2.waitKey(1)

		return car_locations


def waitForSignal():
	Server.calibration = None  # Reset calibration.
	Server.car_identification = None # Reset car identification.
	Server.latest_data = None # Reset latest tracking data.
	# Wait for signal from controller.
	while not Server.isConnected:
		pass

def calibrate(cam, calibrator):
	while True:
		if not Server.isConnected:
			break
		frame = cam.get_frame()
		if frame is None:
			continue
		pt, corners = calibrator.get_transform(frame)
		if pt is not None:
			BaselineTracker.perspective_transform = pt
			Server.calibration = corners
			break


def track(cam, tracker):
	while True:
		if not Server.isConnected:
			break
		frame = cam.get_frame()
		if frame is None:
			continue
		Server.latest_data = tracker.track_cars(frame)

if __name__ == "__main__":
	# GETTING THE HUE VALUES RIGHT
	img = cv2.imread("test.png")
	hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	orange = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
	red = cv2.inRange(hsv_img, RED_MIN, RED_MAX)
	green = cv2.inRange(hsv_img, GREEN_MIN, GREEN_MAX)
	pink = cv2.inRange(hsv_img, PINK_MIN, PINK_MAX)

	cv2.imshow("orange", orange)
	cv2.imshow("red", red)
	cv2.imshow("green", green)
	cv2.imshow("pink", pink)
	cv2.waitKey(0)

	exit()

	_ = Server()
	while True:
		print("Started listen loop.")
		cam = Camera()
		calibrator = Calibrator()
		tracker = BaselineTracker()
		waitForSignal()
		# Calibrate first.
		calibrate(cam, calibrator)
		cv2.destroyAllWindows()
		# Get background image.
		time.sleep(8)
		tracker.background = cam.get_frame()
		# Start tracking.
		track(cam, tracker)
		cv2.destroyAllWindows()
		cam.destroy()