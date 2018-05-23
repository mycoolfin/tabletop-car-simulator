import cv2
import time


CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480

class Camera:
    def __init__(self):
        self.stream = cv2.VideoCapture(0)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)
    def get_frame(self):
        _, frame = self.stream.read()
        return frame
    def destroy(self):
        self.stream.release()
        cv2.destroyAllWindows()
