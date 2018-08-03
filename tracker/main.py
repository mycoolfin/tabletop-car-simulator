from camera import Camera
from calibrator import Calibrator
from cartracker import CarTracker
from server import Server
import cv2
import time



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
            CarTracker.perspective_transform = pt
            Server.calibration = corners
            break

def identify(cam, tracker):
    while True:
        if not Server.isConnected:
            break
        frame = cam.get_frame()
        if frame is None:
            continue
        num_cars_found = tracker.lock_on(frame)
        if num_cars_found is not None:
            Server.car_identification = num_cars_found
            break

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
        calibrator = Calibrator()
        tracker = CarTracker()
        waitForSignal()
        # Calibrate first.
        calibrate(cam, calibrator)
        cv2.destroyAllWindows()
        # Identify car starting positions.
        identify(cam, tracker)
        cv2.destroyAllWindows()
        # Start tracking.
        track(cam, tracker)
        cv2.destroyAllWindows()
        cam.destroy()


if __name__ == "__main__":
    main()