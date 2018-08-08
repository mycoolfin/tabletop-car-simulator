import cv2
from threading import Thread
import time


CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480

class Camera:
	def __init__(self):
		self.stream = cv2.VideoCapture(0)
		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)

		_, self.frame = self.stream.read()
		self.stopped = False

		self.start()

	def start(self):
		Thread(target=self.update, args=()).start()
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