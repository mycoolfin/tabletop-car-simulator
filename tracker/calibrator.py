import cv2
import numpy as np
import pygame
import os
import time
import math

msgHeader = "[CALIBRATOR]: "

DISPLAY_WIDTH = 1600
DISPLAY_HEIGHT = 1200

CALIBRATION_IMG_PATH = os.path.join(os.path.dirname(__file__), '..',
                                    'resources', 'media', 'calibration', 'checkerboard.png')

class Calibrator:
    def get_transform(self, inputImage):
        print(msgHeader + "Attempting to calibrate...")
        start = time.time()
        img1 = cv2.imread(CALIBRATION_IMG_PATH)
        img2 = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)

        patternSize = (10,7)

        _, reference_corners = cv2.findChessboardCorners(img1, patternSize)
        found, projected_corners = cv2.findChessboardCorners(img2, patternSize)

        if found:
            rc = np.array(reference_corners).reshape(len(reference_corners), 2)
            pc = np.array(projected_corners).reshape(len(projected_corners), 2)

            homo = cv2.findHomography(pc, rc)
            cam_corners = self.calculate_corners(pc)
            world_corners = self.calculate_corners(pc, homo[0])
            corners = [cam_corners, world_corners]
            end = time.time()
            print(msgHeader + "Successfully calibrated in " + str(round(end-start, 2)) + " seconds.")


            warped = cv2.resize(cv2.warpPerspective(inputImage, homo[0], (1600,1200)), (640, 480))
            two = np.concatenate((inputImage, warped), axis=1)

            cv2.namedWindow("cal")
            cv2.moveWindow("cal", 100,100)
            cv2.imshow("cal", two)
            cv2.waitKey(1)

            return homo[0], corners
        else:
            print(msgHeader + "Could not calibrate.")
            return None, None

    def calculate_corners(self, pc, mat=None):
        corners = []
        index = 0
        for p in pc:
            if index == 0 or index == 9 or index == 60 or index == 69:
                if mat is not None:
                    point = np.matrix([p[0], p[1], 1]).T
                    hPoint = np.dot(mat, point)
                    x = int(hPoint[0])
                    y = int(hPoint[1])
                else:
                    x = int(p[0] * 2.5)
                    y = int(p[1] * 2.5)
                corners.append((x,y))
            index += 1

        x1, y1 = corners[0]
        x2, y2 = corners[1]
        x3, y3 = corners[2]
        x4, y4 = corners[3]
        sw = int(math.hypot(x2-x1,y2-y1) / 9)
        xAngle = math.atan2(y2-y1, x2-x1)
        yAngle = math.atan2(y3-y1, x3-x1)
        xLeft = -sw*math.cos(xAngle)
        yUp = -sw*math.sin(yAngle)
        xRight = sw*math.cos(xAngle)
        yDown = sw*math.sin(yAngle)

        print(xLeft,xRight,yUp,yDown)

        tl = [x1 + xLeft, y1 + yUp]
        tr = [x2 + xRight, y2 + yUp]
        bl = [x3 + xLeft, y3 + yDown]
        br = [x4 + xRight, y4 + yDown]

        return [tl, tr, bl, br]
