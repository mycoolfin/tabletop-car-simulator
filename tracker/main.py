from camera import Camera
from cartracker import CarTracker
from server import Server
import cv2
import time


def waitForSignal():
	Server.calibration = None  # Reset calibration.
	Server.car_identification = None  # Reset car identification.
	Server.latest_data = None  # Reset latest tracking data.
	# Wait for signal from controller.
	while not Server.isConnected:
		pass


def track(cam, tracker):
	while True:
		if not Server.isConnected:
			break
		frame = cam.get_frame()
		if frame is None:
			continue
		Server.latest_data = tracker.track_cars(frame)

def main():
	_ = Server()
	while True:
		print("Started listen loop.")
		cam = Camera()
		tracker = CarTracker()
		waitForSignal()
		# Start tracking.
		track(cam, tracker)
		cv2.destroyAllWindows()
		cam.destroy()


if __name__ == "__main__":
	main()
