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
		bg_img = self.background.copy()
		bg_gray = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		frame_diff = cv2.absdiff(gray, bg_gray)
		_, thresh = cv2.threshold(frame_diff, 10, 255, cv2.THRESH_BINARY)

		fg_img = cv2.bitwise_and(image, image, mask=thresh)

		cv2.imshow("thresh", thresh)
		cv2.imshow("fg", fg_img)
		cv2.waitKey(1)

		return None


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
		time.sleep(2)
		tracker.background = cam.get_frame()
		# Start tracking.
		track(cam, tracker)
		cv2.destroyAllWindows()
		cam.destroy()