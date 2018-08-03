import cv2
import numpy as np
import pygame
import os
import time

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
        xMin = None
        xMax = None
        yMin = None
        yMax = None
        for p in pc:
            if mat is not None:
                point = np.matrix([p[0], p[1], 1]).T
                hPoint = np.dot(mat, point)
                x = hPoint[0]
                y = hPoint[1]
            else:
                x = int(p[0] * 2.5)
                y = int(p[1] * 2.5)
            if xMin is None or x < xMin:
                xMin = int(x)
            if xMax is None or x > xMax:
                xMax = int(x)
            if yMin is None or y < yMin:
                yMin = int(y)
            if yMax is None or y > yMax:
                yMax = int(y)

        sw = int((xMin - xMax) / 9)

        tl = [xMin + sw, yMin + sw]
        tr = [xMax - sw, yMin + sw]
        bl = [xMin + sw, yMax - sw]
        br = [xMax - sw, yMax - sw]

        return [tl, tr, bl, br]




    def OBSOLETE_show_differences(self, pc, mat):
        xMin = None
        xMax = None
        yMin = None
        yMax = None
        for p in pc:
            x = int(p[0] * 2)
            y = int(p[1] * 2)
            if xMin is None or x < xMin:
                xMin = x
            if xMax is None or x > xMax:
                xMax = x
            if yMin is None or y < yMin:
                yMin = y
            if yMax is None or y > yMax:
                yMax = y

        sw = int((xMin - xMax) / 9)

        tl = [xMin + sw, yMin + sw]
        tr = [xMax - sw, yMin + sw]
        bl = [xMin + sw, yMax - sw]
        br = [xMax - sw, yMax - sw]

        pygame.draw.line(self.screen, (255, 0, 0), tl, tr, 5)
        pygame.draw.line(self.screen, (255, 0, 0), tl, bl, 5)
        pygame.draw.line(self.screen, (255, 0, 0), bl, br, 5)
        pygame.draw.line(self.screen, (255, 0, 0), br, tr, 5)

        xMin = None
        xMax = None
        yMin = None
        yMax = None
        for p in pc:
            point = np.matrix([p[0], p[1], 1]).T
            hPoint = np.dot(mat, point)
            x = hPoint[0]
            y = hPoint[1]
            if xMin is None or x < xMin:
                xMin = x
            if xMax is None or x > xMax:
                xMax = x
            if yMin is None or y < yMin:
                yMin = y
            if yMax is None or y > yMax:
                yMax = y

        sw = int((xMin - xMax) / 9)

        tl = [xMin + sw, yMin + sw]
        tr = [xMax - sw, yMin + sw]
        bl = [xMin + sw, yMax - sw]
        br = [xMax - sw, yMax - sw]

        pygame.draw.line(self.screen, (0, 255, 0), tl, tr, 5)
        pygame.draw.line(self.screen, (0, 255, 0), tl, bl, 5)
        pygame.draw.line(self.screen, (0, 255, 0), bl, br, 5)
        pygame.draw.line(self.screen, (0, 255, 0), br, tr, 5)




