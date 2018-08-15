import cv2
from threading import Thread
import os
import time


CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480

camSetupScript = 	"""
					v4l2-ctl \
					-c auto_exposure=1 \
					-c exposure_time_absolute=100 \
					-c white_balance_auto_preset=0 \
					-c red_balance=2300 \
					-c blue_balance=1400
					"""
# G04 values are red=2000 blue=1500


class Camera:
	def __init__(self):
		os.system(camSetupScript)
		self.stream = cv2.VideoCapture(0)
		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)

		_, self.frame = self.stream.read()
		self.stopped = False

		self.start()

	def start(self):
		t_process = Thread(target=self.update)
		t_process.daemon = True
		t_process.start()
		return self

	def update(self):
		while True:
			if self.stopped:
				return
			_, self.frame = self.stream.read()

	def get_frame(self):
		return self.frame

	def stop(self):
		self.stopped = True

	def destroy(self):
		self.stop()
		self.stream.release()


if __name__ == "__main__":
	cam = Camera()
	while True:
		cv2.imshow("", cam.get_frame())
		cv2.waitKey(1)